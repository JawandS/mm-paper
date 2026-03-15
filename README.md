# Clustering

Produces all data and figures for: **"Do Embedding-Based Clusters Recover CIP Academic Areas?"**

Clusters raw CIP program descriptions using embeddings and measures how well those clusters recover the 2-digit CIP area labels (ARI, NMI, purity, silhouette).

## Setup

```bash
cp ../.env .env          # needs OPENAI_API_KEY
uv sync
```

## Run

```bash
uv run python 0_prepare/main.py    # filter CIP taxonomy → data/clean_majors.csv
uv run python 0_prepare/remove_invalid_cip_codes.py  # remove reserved/non-IPEDS CIP codes from clean_majors + embeddings
uv run python 1_embed/main.py      # embed programs    → data/embeddings.json
uv run python 2a_unsupervised/kmeans.py  # unsupervised clustering → data/results/metrics_k12.csv
uv run python 2b_supervised/main.py      # supervised benchmark     → data/results/supervised/
```

Notes:
- `0_prepare/remove_invalid_cip_codes.py` removes CIP rows explicitly marked as
  `Reserved for use by Statistics Canada` / `not valid for IPEDS reporting`.
- The same CIP codes are removed from both `data/clean_majors.csv` and
  `data/embeddings.json` to keep datasets aligned.

## Scope

- Input: `CIPCode2020.csv` — title + definition text per program
- Ground truth: 2-digit CIP area (12 areas, ~1,100 programs)
- Embedding model: `text-embedding-3-large` (3,072 dims)
- Clustering: spherical k-means, k=2–30, 10 seeds each
- Figures: silhouette by k, ARI+NMI by k, purity by k, UMAP by CIP area, UMAP by k=12 cluster
