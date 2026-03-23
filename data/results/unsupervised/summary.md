# Clustering Results

**k=23, spherical k-means, 100 seeds**

## Summary

| Strategy | n | ARI | NMI | Purity |
|---|---|---|---|---|
| random     | 100 | 0.424 ± 0.032 | 0.659 ± 0.020 | 0.686 ± 0.025 |
| stratified | 100 | 0.477 ± 0.031 | 0.688 ± 0.019 | 0.719 ± 0.025 |
| cip_mean   |   1 | 0.656 | 0.798 | 0.838 |

## Delta vs Random (mean)

| Strategy | ΔARI | ΔNMI | ΔPurity |
|---|---|---|---|
| stratified | +0.053 | +0.029 | +0.034 |
| cip_mean | +0.231 | +0.139 | +0.152 |

## Range (min – max) across 100 seeds

| Strategy | ARI | NMI | Purity |
|---|---|---|---|
| random     | 0.347 – 0.505 | 0.607 – 0.695 | 0.632 – 0.744 |
| stratified | 0.389 – 0.549 | 0.634 – 0.735 | 0.627 – 0.788 |

## Strategy Definitions

- **random**: k programs chosen uniformly at random as initial centroids
- **stratified**: one random program per CIP group as initial centroid (no group represented twice)
- **cip_mean**: normalized mean embedding per CIP group as initial centroid (deterministic, run once)
