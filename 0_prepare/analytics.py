"""Generate a CIP cluster summary from clean majors data.

This script reads ``data/clean_majors.csv`` and overwrites ``data/cip_areas.md``
with:
- total number of CIP 2-digit clusters
- total number of majors
- per-cluster major counts and CIP area names
"""

from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
INPUT_FILE = DATA_DIR / "clean_majors.csv"
TAXONOMY_FILE = DATA_DIR / "CIPCode2020.csv"
OUTPUT_FILE = DATA_DIR / "cip_areas.md"


def clean_code(value: str) -> str:
    """Normalize CIP values exported with Excel-style quoting."""
    return value.strip().replace('="', "").replace('"', "")


def load_area_names() -> dict[str, str]:
    """Return mapping from 2-digit CIP area code to official CIP area title."""
    taxonomy = pd.read_csv(TAXONOMY_FILE, dtype=str)
    taxonomy["CIPCode"] = taxonomy["CIPCode"].fillna("").apply(clean_code)
    taxonomy["CIPTitle"] = taxonomy["CIPTitle"].fillna("").str.strip()

    # Area-level rows are the 2-digit codes (e.g., "01").
    area_rows = taxonomy[taxonomy["CIPCode"].str.fullmatch(r"\d{2}")].copy()
    return dict(zip(area_rows["CIPCode"], area_rows["CIPTitle"]))


def main() -> None:
    """Build and write markdown summary for CIP 2-digit cluster counts."""
    df = pd.read_csv(INPUT_FILE, dtype=str)
    df["CIPArea"] = df["CIPArea"].fillna("").str.strip()
    area_names = load_area_names()

    counts = (
        df.groupby("CIPArea")
        .size()
        .reset_index(name="num_majors")
        .sort_values(["num_majors", "CIPArea"], ascending=[False, True])
        .reset_index(drop=True)
    )
    counts["CIPName"] = counts["CIPArea"].map(area_names).fillna("Unknown")

    total_clusters = counts["CIPArea"].nunique()
    total_majors = int(counts["num_majors"].sum())

    lines = [
        "# CIP Areas (2-Digit Cluster Counts)",
        "",
        f"- Total clusters: **{total_clusters}**",
        f"- Total majors: **{total_majors}**",
        "",
        "| Cluster ID (CIPArea) | CIP Name | Number of majors |",
        "|---|---|---:|",
    ]

    for row in counts.itertuples(index=False):
        lines.append(f"| `{row.CIPArea}` | {row.CIPName} | {int(row.num_majors)} |")

    OUTPUT_FILE.write_text("\n".join(lines) + "\n")
    print(f"Wrote summary to {OUTPUT_FILE}")
    print(f"Total clusters: {total_clusters}")
    print(f"Total majors: {total_majors}")


if __name__ == "__main__":
    main()
