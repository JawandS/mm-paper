# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Research analysis pipeline for the paper **"Do Embedding-Based Clusters Recover CIP Academic Areas?"** — clusters CIP (Classification of Instructional Programs) program descriptions using OpenAI embeddings and measures cluster quality against 2-digit CIP area ground truth labels (ARI, NMI, purity, silhouette).

## Setup

```bash
cp ../.env .env   # needs OPENAI_API_KEY
uv sync
```

## Pipeline Commands

The pipeline runs in stages; each stage depends on prior outputs:

```bash
uv run python 0_prepare/main.py                                             # → data/clean_majors.csv
uv run python 0_prepare/remove_invalid_cip_codes.py                        # mutates clean_majors.csv + embeddings.json in-place
uv run python 1_embed/main.py                                              # → data/embeddings.json (resumable)
uv run python 2a_unsupervised/kmeans.py                                    # → data/results/unsupervised/
uv run python 2a_unsupervised/cluster_analysis/export_cip_mean_labels.py   # → cip_mean_labels_k12.csv + centroids JSON
uv run python 2a_unsupervised/cluster_analysis/build_cluster_analysis_md.py # → cluster_analysis.md
uv run python 2b_supervised/main.py                                        # → data/results/supervised/
```

## Architecture

The repo is a linear research pipeline, not an application:

- **`0_prepare/`** — Filter `CIPCode2020.csv` to 1,264 programs across 23 CIP areas (excludes stubs, residency areas 60/61, reserved/IPEDS-invalid codes)
- **`1_embed/`** — Embed each program's title + definition using `text-embedding-3-large` (3,072 dims) via OpenAI API; writes incrementally so it can resume
- **`2a_unsupervised/`** — Spherical k-means with 3 init strategies (random, stratified, cip_mean); tests k=2–30 with 10 seeds; ground truth is 12 2-digit CIP areas
- **`2b_supervised/`** — Supervised benchmark (logistic regression, SVM RBF, MLP ± PCA) with 5-fold stratified CV for comparison against unsupervised metrics
- **`thesis/`** — LaTeX source for the paper itself

Key data files (not committed if large):
- `data/embeddings.json` — keyed by CIP code, values are 3,072-dim float arrays
- `data/clean_majors.csv` — CIP code, 2-digit area, title, definition
- `data/results/unsupervised/metrics_k12.csv` — per-seed ARI/NMI/purity results

When `remove_invalid_cip_codes.py` runs, it must keep `clean_majors.csv` and `embeddings.json` in sync (same set of CIP codes in both files).

## Paper Writing

The `thesis/` directory contains the LaTeX paper. Recent git history shows active writing work; the pipeline scripts are mostly stable. The paper's ground truth uses **12 CIP areas** (not 23 — filtered down from the full taxonomy).
