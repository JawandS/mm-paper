"""Build a per-cluster Markdown analysis for cip_mean labels.

For each named cluster, the report includes:
- The major closest to the cluster centroid
- The major farthest from the cluster centroid
- Centroid drift from initialization
- Nearest cluster for the farthest major
"""

import json
import re
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"
INPUT_FILE = DATA_DIR / "results" / "unsupervised" / "cluster_analysis" / "cip_mean_labels_k12.csv"
CENTROIDS_FILE = DATA_DIR / "results" / "unsupervised" / "cluster_analysis" / "cip_mean_centroids_k12.json"
AREAS_FILE = DATA_DIR / "cip_areas.md"
OUTPUT_FILE = DATA_DIR / "results" / "unsupervised" / "cluster_analysis" / "cluster_analysis.md"


def _quote_block(text: str) -> str:
    """Render multi-line text as a markdown blockquote."""
    safe_text = str(text).strip().replace("\r\n", "\n").replace("\r", "\n")
    return "\n".join(f"> {line}" if line else ">" for line in safe_text.split("\n"))


def _major_section(label: str, row: pd.Series) -> list[str]:
    """Format one major record for markdown output."""
    return [
        f"### {label}",
        f"- CIPCode: `{row['CIPCode']}`",
        f"- CIPTitle: {row['CIPTitle']}",
        f"- DistanceToCentroid: `{float(row['DistanceToCentroid']):.4f}`",
        "- CIPDefinition:",
        _quote_block(row["CIPDefinition"]),
        "",
    ]


def _major_section_from_dict(label: str, major: dict, distance: float) -> list[str]:
    """Format one major record (dict source) for markdown output."""
    return [
        f"### {label}",
        f"- CIPCode: `{major['CIPCode']}`",
        f"- CIPTitle: {major['CIPTitle']}",
        f"- DistanceToCentroid: `{float(distance):.4f}`",
        "- CIPDefinition:",
        _quote_block(major["CIPDefinition"]),
        "",
    ]


def load_area_code_by_name() -> dict[str, str]:
    """Parse CIP area name -> 2-digit area code from markdown."""
    pattern = re.compile(r"-\s+`(?P<code>\d{2})`:\s+(?P<name>.+)")
    mapping: dict[str, str] = {}
    for line in AREAS_FILE.read_text().splitlines():
        match = pattern.match(line.strip())
        if match:
            area_name = match.group("name").strip().rstrip(".")
            mapping[area_name] = match.group("code")
    if not mapping:
        raise ValueError(f"No area mappings found in {AREAS_FILE}")
    return mapping


def main() -> None:
    df = pd.read_csv(INPUT_FILE, dtype=str)
    centroid_payload = json.loads(CENTROIDS_FILE.read_text())
    area_code_by_name = load_area_code_by_name()
    if df.empty:
        raise ValueError(f"No rows found in {INPUT_FILE}")
    if "ClusterName" not in df.columns:
        raise ValueError("Expected 'ClusterName' column in labels CSV.")
    df["DistanceToCentroid"] = pd.to_numeric(df["DistanceToCentroid"])
    centroid_info_by_name = {
        row["cluster_name"]: row for row in centroid_payload.get("centroids", [])
    }

    lines: list[str] = []
    lines.append("# Cluster Analysis")
    lines.append("")
    lines.append(
        "Closest/farthest majors, composition stats, centroid drift, and farthest-major nearest-cluster checks for `cip_mean` (`k=12`)."
    )
    lines.append("")

    for cluster_name in sorted(df["ClusterName"].unique()):
        cluster = df[df["ClusterName"] == cluster_name].copy()
        if cluster.empty:
            continue
        centroid_info = centroid_info_by_name.get(cluster_name)
        if centroid_info is None:
            raise ValueError(f"Missing centroid info for cluster: {cluster_name}")

        # Stable tie-breakers keep output deterministic.
        closest = cluster.sort_values(
            by=["DistanceToCentroid", "CIPCode"], ascending=[True, True]
        ).iloc[0]
        farthest_major = centroid_info["farthest_major"]
        cluster_size = len(cluster)
        area_counts = cluster["CIPArea"].value_counts().sort_values(ascending=False)
        dominant_area = str(area_counts.index[0])
        dominant_count = int(area_counts.iloc[0])
        dominant_pct = 100.0 * dominant_count / cluster_size
        named_area_code = area_code_by_name.get(cluster_name)
        named_area_count = (
            int((cluster["CIPArea"] == named_area_code).sum())
            if named_area_code is not None
            else 0
        )
        named_area_pct = 100.0 * named_area_count / cluster_size
        top3 = area_counts.head(3)
        top3_str = ", ".join(
            f"{code}: {count} ({100.0 * count / cluster_size:.1f}%)"
            for code, count in top3.items()
        )
        distance_stats = cluster["DistanceToCentroid"].astype(float)

        lines.append(f"## {cluster_name}")
        lines.append("")
        lines.append("### Composition Stats")
        lines.append(f"- Cluster size: `{cluster_size}`")
        lines.append(f"- Distinct CIP areas in cluster: `{cluster['CIPArea'].nunique()}`")
        lines.append(
            f"- Dominant CIP area share: `{dominant_pct:.1f}%` (area `{dominant_area}`, {dominant_count}/{cluster_size})"
        )
        if named_area_code is not None:
            lines.append(
                f"- Share matching cluster CIP area `{named_area_code}`: `{named_area_pct:.1f}%` ({named_area_count}/{cluster_size})"
            )
        lines.append(f"- Top area mix: {top3_str}")
        lines.append(
            f"- Distance to centroid (mean/median/std): `{distance_stats.mean():.4f}` / `{distance_stats.median():.4f}` / `{distance_stats.std():.4f}`"
        )
        lines.append(
            f"- Distance to centroid (min/p90/max): `{distance_stats.min():.4f}` / `{distance_stats.quantile(0.90):.4f}` / `{distance_stats.max():.4f}`"
        )
        lines.append("")
        lines.append("### Centroid Shift From Initialization")
        lines.append(
            f"- Cosine distance: `{float(centroid_info['centroid_shift_from_initialization']['cosine_distance']):.6f}`"
        )
        lines.append(
            f"- L2 delta: `{float(centroid_info['centroid_shift_from_initialization']['l2_delta']):.6f}`"
        )
        lines.append("")
        lines.extend(_major_section("Closest To Centroid", closest))
        lines.extend(
            _major_section_from_dict(
                "Farthest From Centroid",
                farthest_major,
                farthest_major["assigned_cluster_distance"],
            )
        )
        nearest_overall = farthest_major["nearest_cluster_overall"]
        nearest_other = farthest_major["nearest_other_cluster"]
        lines.append("### Farthest-Major Nearest Cluster")
        lines.append(
            f"- Major: `{farthest_major['CIPCode']}` {farthest_major['CIPTitle']}"
        )
        lines.append(
            f"- Assigned cluster distance: `{float(farthest_major['assigned_cluster_distance']):.6f}`"
        )
        lines.append(
            f"- Nearest cluster (overall): `{nearest_overall['cluster_name']}` (distance `{float(nearest_overall['distance']):.6f}`)"
        )
        lines.append(
            f"- Nearest other cluster: `{nearest_other['cluster_name']}` (distance `{float(nearest_other['distance']):.6f}`)"
        )
        lines.append("")

    OUTPUT_FILE.write_text("\n".join(lines).rstrip() + "\n")
    print(f"Saved cluster analysis to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
