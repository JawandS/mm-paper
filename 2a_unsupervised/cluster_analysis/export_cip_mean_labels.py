"""Export per-major CIP-mean cluster labels and centroid JSON.

This script reproduces the deterministic `cip_mean` clustering setup from
`2a_unsupervised/kmeans.py` (k=12, spherical k-means), then writes a CSV based on
`data/clean_majors.csv` with cluster naming columns:
- ClusterName: cluster label mapped from `data/cip_areas.md`
- DistanceToCentroid: cosine distance to the assigned cluster centroid (rounded)

Also writes a JSON file with centroid calculation details for each cluster, plus:
- Centroid drift from initialization to final centroid
- For the farthest major in each cluster, the nearest cluster(s)
"""

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"
CLEAN_FILE = DATA_DIR / "clean_majors.csv"
EMBEDDINGS_FILE = DATA_DIR / "embeddings.json"
AREAS_FILE = DATA_DIR / "cip_areas.md"
OUTPUT_DIR = DATA_DIR / "results" / "unsupervised" / "cluster_analysis"
LABELS_OUTPUT_FILE = OUTPUT_DIR / "cip_mean_labels_k12.csv"
CENTROIDS_OUTPUT_FILE = OUTPUT_DIR / "cip_mean_centroids_k12.json"

K = 12
DISTANCE_DECIMALS = 4


def load_area_names() -> dict[str, str]:
    """Parse CIP area code -> area name mapping from markdown."""
    pattern = re.compile(r"-\s+`(?P<code>\d{2})`:\s+(?P<name>.+)")
    mapping: dict[str, str] = {}
    for line in AREAS_FILE.read_text().splitlines():
        match = pattern.match(line.strip())
        if match:
            mapping[match.group("code")] = match.group("name").strip().rstrip(".")
    if not mapping:
        raise ValueError(f"No area mappings found in {AREAS_FILE}")
    return mapping


def normalize(vectors: np.ndarray) -> np.ndarray:
    """Row-normalize vectors to unit length."""
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors / np.clip(norms, 1e-12, None)


def cip_centroids(x: np.ndarray, area_ids: np.ndarray, k: int) -> np.ndarray:
    """Initialize one centroid per CIP area using normalized area means."""
    centroids = np.zeros((k, x.shape[1]))
    for i in range(k):
        group = x[area_ids == i]
        mean = group.mean(axis=0)
        centroids[i] = mean / np.clip(np.linalg.norm(mean), 1e-12, None)
    return centroids


def spherical_kmeans_with_centroids(
    x: np.ndarray, k: int, initial_centroids: np.ndarray, seed: int
) -> tuple[np.ndarray, np.ndarray]:
    """Run spherical k-means and return final labels and normalized centroids."""
    rng = np.random.default_rng(seed)
    centroids = initial_centroids.copy()

    for _ in range(300):
        labels = np.argmax(x @ centroids.T, axis=1)
        new_centroids = np.zeros_like(centroids)

        for i in range(k):
            cluster = x[labels == i]
            if cluster.size == 0:
                new_centroids[i] = x[rng.integers(0, x.shape[0])]
            else:
                mean = cluster.mean(axis=0)
                new_centroids[i] = mean / np.clip(np.linalg.norm(mean), 1e-12, None)

        if np.linalg.norm(centroids - new_centroids) < 1e-4:
            centroids = new_centroids
            break

        centroids = new_centroids

    final_labels = np.argmax(x @ centroids.T, axis=1)
    return final_labels, centroids


def main() -> None:
    df = pd.read_csv(CLEAN_FILE, dtype=str)
    embeddings = json.loads(EMBEDDINGS_FILE.read_text())
    area_name_map = load_area_names()

    # Keep only rows with available embeddings to align with clustering input.
    df = df[df["CIPCode"].isin(embeddings)].reset_index(drop=True)
    x = normalize(np.array([embeddings[code] for code in df["CIPCode"]], dtype=float))
    area_ids, area_index = pd.factorize(df["CIPArea"].values)

    if len(area_index) != K:
        raise ValueError(f"Expected {K} CIP areas, found {len(area_index)}")

    # area_index order is aligned with centroid index during cip_mean init.
    cluster_name_by_index = {
        idx: area_name_map.get(code, f"Unknown Area {code}")
        for idx, code in enumerate(area_index.astype(str))
    }

    initial_centroids = cip_centroids(x, area_ids, K)
    labels, centroids = spherical_kmeans_with_centroids(
        x=x,
        k=K,
        initial_centroids=initial_centroids,
        seed=0,
    )

    # For normalized vectors, cosine distance is 1 - cosine similarity.
    cosine_similarity = np.sum(x * centroids[labels], axis=1)
    raw_distances = 1.0 - cosine_similarity
    distances = np.round(raw_distances, DISTANCE_DECIMALS)

    out = df.copy()
    out["ClusterName"] = pd.Series(labels).map(cluster_name_by_index)
    out["DistanceToCentroid"] = distances

    centroid_rows = []
    for cluster_idx in range(K):
        cluster_mask = labels == cluster_idx
        members = x[cluster_mask]
        if members.size == 0:
            continue
        mean_vector = members.mean(axis=0)
        mean_norm = float(np.linalg.norm(mean_vector))

        init_centroid = initial_centroids[cluster_idx]
        final_centroid = centroids[cluster_idx]
        shift_cosine_distance = float(1.0 - np.dot(init_centroid, final_centroid))
        shift_l2_delta = float(np.linalg.norm(final_centroid - init_centroid))

        member_indices = np.where(cluster_mask)[0]
        # Deterministic tie-break: max distance, then lexical CIPCode.
        farthest_idx = max(
            member_indices,
            key=lambda idx: (raw_distances[idx], str(df.loc[idx, "CIPCode"])),
        )
        farthest_embedding = x[farthest_idx]
        similarities = centroids @ farthest_embedding

        nearest_cluster_index = int(np.argmax(similarities))
        nearest_cluster_distance = float(1.0 - similarities[nearest_cluster_index])

        other_indices = [i for i in range(K) if i != cluster_idx]
        nearest_other_index = max(other_indices, key=lambda i: similarities[i])
        nearest_other_distance = float(1.0 - similarities[nearest_other_index])

        centroid_rows.append(
            {
                "cluster_index": cluster_idx + 1,
                "cluster_name": cluster_name_by_index[cluster_idx],
                "member_count": int(members.shape[0]),
                "calculation": {
                    "formula": "centroid = mean(cluster_embeddings) / ||mean(cluster_embeddings)||_2",
                    "mean_vector_l2_norm": mean_norm,
                },
                "centroid_shift_from_initialization": {
                    "cosine_distance": shift_cosine_distance,
                    "l2_delta": shift_l2_delta,
                },
                "farthest_major": {
                    "CIPCode": str(df.loc[farthest_idx, "CIPCode"]),
                    "CIPTitle": str(df.loc[farthest_idx, "CIPTitle"]),
                    "CIPDefinition": str(df.loc[farthest_idx, "CIPDefinition"]),
                    "assigned_cluster_distance": float(raw_distances[farthest_idx]),
                    "nearest_cluster_overall": {
                        "cluster_index": nearest_cluster_index + 1,
                        "cluster_name": cluster_name_by_index[nearest_cluster_index],
                        "distance": nearest_cluster_distance,
                    },
                    "nearest_other_cluster": {
                        "cluster_index": nearest_other_index + 1,
                        "cluster_name": cluster_name_by_index[nearest_other_index],
                        "distance": nearest_other_distance,
                    },
                },
                "centroid": centroids[cluster_idx].tolist(),
            }
        )

    centroid_payload = {
        "method": "cip_mean",
        "k": K,
        "distance_metric": "cosine_distance = 1 - cosine_similarity",
        "centroids": centroid_rows,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out.to_csv(LABELS_OUTPUT_FILE, index=False)
    CENTROIDS_OUTPUT_FILE.write_text(json.dumps(centroid_payload, indent=2) + "\n")
    print(f"Saved {len(out)} rows to {LABELS_OUTPUT_FILE}")
    print(f"Saved centroid JSON to {CENTROIDS_OUTPUT_FILE}")


if __name__ == "__main__":
    main()
