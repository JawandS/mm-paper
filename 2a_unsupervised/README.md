# 2a Unsupervised

This directory runs the unsupervised clustering analysis used in the paper.

## What It Does

- Builds spherical k-means clusters over program embeddings (`k=12` in `kmeans.py`)
- Compares cluster assignments to CIP area labels (ARI, NMI, purity)
- Exports detailed `cip_mean` cluster-analysis artifacts (labels, centroids, markdown report)

## Scripts

- `kmeans.py`
  - Main unsupervised benchmark.
  - Runs multiple initialization strategies (`random`, `stratified`, `cip_mean`).
  - Writes summary metrics and markdown.

- `cluster_analysis/export_cip_mean_labels.py`
  - Re-runs deterministic `cip_mean` (`k=12`, seed `0`).
  - Exports per-major labels and centroid distance.
  - Exports centroid JSON with:
    - Final centroids
    - Centroid shift from initialization
    - Farthest-major nearest-cluster calculations

- `cluster_analysis/build_cluster_analysis_md.py`
  - Builds a human-readable markdown report per cluster.
  - Includes closest/farthest major, centroid shift, and nearest-cluster info.

## Inputs

- `data/clean_majors.csv`
- `data/embeddings.json`
- `data/cip_areas.md`

## Outputs

- `data/results/unsupervised/metrics_k12.csv`
- `data/results/unsupervised/summary.md`
- `data/results/unsupervised/cluster_analysis/cip_mean_labels_k12.csv`
- `data/results/unsupervised/cluster_analysis/cip_mean_centroids_k12.json`
- `data/results/unsupervised/cluster_analysis/cluster_analysis.md`

## Run

```bash
uv run python 2a_unsupervised/kmeans.py
uv run python 2a_unsupervised/cluster_analysis/export_cip_mean_labels.py
uv run python 2a_unsupervised/cluster_analysis/build_cluster_analysis_md.py
```
