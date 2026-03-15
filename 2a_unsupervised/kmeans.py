import json
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
CLEAN_FILE = DATA_DIR / "clean_majors.csv"
EMBEDDINGS_FILE = DATA_DIR / "embeddings.json"
OUTPUT_DATA = DATA_DIR / "results" / "unsupervised"
METRICS_FILE = OUTPUT_DATA / "metrics_k12.csv"
SUMMARY_FILE = OUTPUT_DATA / "summary.md"

SEEDS = list(range(100))
K = 23


# --- Clustering ---

def normalize(X):
    norms = np.linalg.norm(X, axis=1, keepdims=True)
    return X / np.clip(norms, 1e-12, None)


def spherical_kmeans(X, k, initial_centroids, seed):
    rng = np.random.default_rng(seed)
    centroids = initial_centroids.copy()
    for _ in range(300):
        labels = np.argmax(X @ centroids.T, axis=1)
        new_centroids = np.zeros_like(centroids)
        for i in range(k):
            cluster = X[labels == i]
            if cluster.size == 0:
                new_centroids[i] = X[rng.integers(0, X.shape[0])]
            else:
                mean = cluster.mean(axis=0)
                new_centroids[i] = mean / np.clip(np.linalg.norm(mean), 1e-12, None)
        if np.linalg.norm(centroids - new_centroids) < 1e-4:
            break
        centroids = new_centroids
    return labels


def random_centroids(X, k, seed):
    rng = np.random.default_rng(seed)
    return X[rng.choice(X.shape[0], size=k, replace=False)]


def cip_centroids(X, area_ids, k):
    centroids = np.zeros((k, X.shape[1]))
    for i in range(k):
        group = X[area_ids == i]
        mean = group.mean(axis=0)
        centroids[i] = mean / np.clip(np.linalg.norm(mean), 1e-12, None)
    return centroids


def stratified_centroids(X, area_ids, k, seed):
    rng = np.random.default_rng(seed)
    centroids = np.zeros((k, X.shape[1]))
    for i in range(k):
        indices = np.where(area_ids == i)[0]
        centroids[i] = X[rng.choice(indices)]
    return centroids


def purity(labels_true, labels_pred):
    return sum(
        np.bincount(labels_true[labels_pred == c]).max()
        for c in np.unique(labels_pred)
    ) / len(labels_true)


def run_and_collect(X, area_ids, init_fn, label):
    rows = []
    for seed in SEEDS:
        pred = spherical_kmeans(X, K, init_fn(seed), seed)
        ari = adjusted_rand_score(area_ids, pred)
        nmi = normalized_mutual_info_score(area_ids, pred)
        pur = purity(area_ids, pred)
        rows.append({"init": label, "seed": seed, "ari": ari, "nmi": nmi, "purity": pur})
        print(f"  [{label}] seed {seed:3d} | ARI={ari:.3f}  NMI={nmi:.3f}  purity={pur:.3f}")
    return rows


# --- Summary ---

def ms(g, col):
    return f"{g[col].mean():.3f} ± {g[col].std():.3f}"

def rng(g, col):
    return f"{g[col].min():.3f} – {g[col].max():.3f}"

def delta(g, col, ref):
    val = (g[col].mean() if g is not None else None) or 0
    return f"{val - ref[col].mean():+.3f}"


def write_summary(rand, strat, cip_row):
    lines = []
    def p(s=""): lines.append(s); print(s)

    p("# Clustering Results")
    p()
    p("**k=12, spherical k-means, 100 seeds**")
    p()
    p("## Summary")
    p()
    p("| Strategy | n | ARI | NMI | Purity |")
    p("|---|---|---|---|---|")
    p(f"| random     | 100 | {ms(rand,'ari')} | {ms(rand,'nmi')} | {ms(rand,'purity')} |")
    p(f"| stratified | 100 | {ms(strat,'ari')} | {ms(strat,'nmi')} | {ms(strat,'purity')} |")
    p(f"| cip_mean   |   1 | {cip_row['ari']:.3f} | {cip_row['nmi']:.3f} | {cip_row['purity']:.3f} |")
    p()
    p("## Delta vs Random (mean)")
    p()
    p("| Strategy | ΔARI | ΔNMI | ΔPurity |")
    p("|---|---|---|---|")
    for label, g in [("stratified", strat), ("cip_mean", None)]:
        vals = [
            f"{((g[col].mean() if g is not None else cip_row[col]) - rand[col].mean()):+.3f}"
            for col in ["ari", "nmi", "purity"]
        ]
        p(f"| {label} | {vals[0]} | {vals[1]} | {vals[2]} |")
    p()
    p("## Range (min – max) across 100 seeds")
    p()
    p("| Strategy | ARI | NMI | Purity |")
    p("|---|---|---|---|")
    p(f"| random     | {rng(rand,'ari')} | {rng(rand,'nmi')} | {rng(rand,'purity')} |")
    p(f"| stratified | {rng(strat,'ari')} | {rng(strat,'nmi')} | {rng(strat,'purity')} |")
    p()
    p("## Strategy Definitions")
    p()
    p("- **random**: k programs chosen uniformly at random as initial centroids")
    p("- **stratified**: one random program per CIP group as initial centroid (no group represented twice)")
    p("- **cip_mean**: normalized mean embedding per CIP group as initial centroid (deterministic, run once)")

    SUMMARY_FILE.write_text("\n".join(lines) + "\n")
    print(f"\nSaved → {SUMMARY_FILE}")


# --- Main ---

def main():
    df = pd.read_csv(CLEAN_FILE, dtype=str)
    embeddings = json.loads(EMBEDDINGS_FILE.read_text())

    df = df[df["CIPCode"].isin(embeddings)].reset_index(drop=True)
    X = normalize(np.array([embeddings[code] for code in df["CIPCode"]], dtype=float))
    area_ids, area_index = pd.factorize(df["CIPArea"].values)

    print(f"Programs: {len(df)}  |  CIP areas: {len(area_index)}  |  k={K}  |  seeds={len(SEEDS)}")

    print("\n[Random initialization]")
    random_rows = run_and_collect(X, area_ids, lambda seed: random_centroids(X, K, seed), "random")

    print("\n[Stratified initialization]")
    strat_rows = run_and_collect(X, area_ids, lambda seed: stratified_centroids(X, area_ids, K, seed), "stratified")

    print("\n[CIP-mean initialization]")
    pred = spherical_kmeans(X, K, cip_centroids(X, area_ids, K), seed=0)
    cip_row = {
        "init": "cip_mean", "seed": 0,
        "ari": adjusted_rand_score(area_ids, pred),
        "nmi": normalized_mutual_info_score(area_ids, pred),
        "purity": purity(area_ids, pred),
    }
    print(f"  [cip_mean] ARI={cip_row['ari']:.3f}  NMI={cip_row['nmi']:.3f}  purity={cip_row['purity']:.3f}")

    # Save metrics CSV
    out_dir = DATA_DIR / "results"
    out_dir.mkdir(exist_ok=True)
    summary_rows = [
        {**pd.DataFrame(random_rows)[["ari","nmi","purity"]].mean().to_dict(), "init": "random_avg", "seed": "avg"},
        {**pd.DataFrame(strat_rows)[["ari","nmi","purity"]].mean().to_dict(), "init": "stratified_avg", "seed": "avg"},
        cip_row,
    ]
    pd.DataFrame(summary_rows + random_rows + strat_rows).to_csv(METRICS_FILE, index=False)
    print(f"\nSaved → {METRICS_FILE}")

    # Save summary markdown
    rand_df = pd.DataFrame(random_rows)
    strat_df = pd.DataFrame(strat_rows)
    print()
    write_summary(rand_df, strat_df, cip_row)


if __name__ == "__main__":
    main()
