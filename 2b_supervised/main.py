import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score
from sklearn.model_selection import StratifiedKFold
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.decomposition import PCA
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.svm import SVC

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
CLEAN_FILE = DATA_DIR / "clean_majors.csv"
EMBEDDINGS_FILE = DATA_DIR / "embeddings.json"
OUTPUT_DIR = DATA_DIR / "results" / "supervised"
METRICS_FILE = OUTPUT_DIR / "metrics.csv"
SUMMARY_FILE = OUTPUT_DIR / "summary.md"

N_SPLITS = 5
RANDOM_SEED = 42


def load_dataset() -> tuple[np.ndarray, np.ndarray, list[str]]:
    """Load embeddings and CIP area labels aligned by CIP code."""
    df = pd.read_csv(CLEAN_FILE, dtype=str)
    embeddings = json.loads(EMBEDDINGS_FILE.read_text())

    df = df[df["CIPCode"].isin(embeddings)].copy().reset_index(drop=True)

    X = np.array([embeddings[code] for code in df["CIPCode"]], dtype=float)
    y_raw = df["CIPArea"].astype(str).to_numpy()

    encoder = LabelEncoder()
    y = encoder.fit_transform(y_raw)

    return X, y, list(encoder.classes_)


def build_models() -> dict[str, object]:
    """Define model pipelines to compare under the same fold splits."""
    return {
        "logistic_regression": make_pipeline(
            StandardScaler(),
            LogisticRegression(
                max_iter=5000,
                class_weight="balanced",
                random_state=RANDOM_SEED,
            ),
        ),
        "logistic_regression_pca95": make_pipeline(
            StandardScaler(),
            PCA(n_components=0.95, svd_solver="full"),
            LogisticRegression(
                max_iter=5000,
                class_weight="balanced",
                random_state=RANDOM_SEED,
            ),
        ),
        "svm_rbf": make_pipeline(
            StandardScaler(),
            SVC(
                kernel="rbf",
                class_weight="balanced",
                random_state=RANDOM_SEED,
            ),
        ),
        "svm_rbf_pca95": make_pipeline(
            StandardScaler(),
            PCA(n_components=0.95, svd_solver="full"),
            SVC(
                kernel="rbf",
                class_weight="balanced",
                random_state=RANDOM_SEED,
            ),
        ),
        "dnn_mlp": make_pipeline(
            StandardScaler(),
            MLPClassifier(
                hidden_layer_sizes=(512, 256),
                activation="relu",
                alpha=1e-4,
                learning_rate_init=1e-3,
                max_iter=500,
                early_stopping=False,
                random_state=RANDOM_SEED,
            ),
        ),
        "dnn_mlp_early_stopping": make_pipeline(
            StandardScaler(),
            MLPClassifier(
                hidden_layer_sizes=(512, 256),
                activation="relu",
                alpha=1e-4,
                learning_rate_init=1e-3,
                max_iter=500,
                early_stopping=True,
                n_iter_no_change=15,
                validation_fraction=0.1,
                random_state=RANDOM_SEED,
            ),
        ),
    }


def evaluate_predictions(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    """Compute core multi-class classification metrics."""
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, average="macro")),
    }


def run_stratified_kfold(
    X: np.ndarray,
    y: np.ndarray,
    models: dict[str, object],
) -> pd.DataFrame:
    """Run stratified k-fold CV for each model and collect train/test metrics."""
    skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=RANDOM_SEED)

    all_rows: list[dict[str, float | int | str]] = []
    for fold_idx, (train_idx, test_idx) in enumerate(skf.split(X, y), start=1):
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]

        print(f"\nFold {fold_idx}/{N_SPLITS} | train={len(train_idx)} test={len(test_idx)}")

        for model_name, model in models.items():
            model.fit(X_train, y_train)

            for split_name, X_split, y_split in (
                ("train", X_train, y_train),
                ("test", X_test, y_test),
            ):
                y_pred = model.predict(X_split)
                metrics = evaluate_predictions(y_split, y_pred)
                all_rows.append(
                    {
                        "model": model_name,
                        "fold": fold_idx,
                        "split": split_name,
                        **metrics,
                    }
                )

                print(
                    f"  {model_name:>20s} | {split_name:>5s} | "
                    f"acc={metrics['accuracy']:.4f} "
                    f"bal_acc={metrics['balanced_accuracy']:.4f} "
                    f"macro_f1={metrics['macro_f1']:.4f}"
                )

    return pd.DataFrame(all_rows)


def write_summary(metrics_df: pd.DataFrame, classes: list[str]) -> None:
    """Write a markdown summary with per-fold and aggregate test metrics."""
    lines: list[str] = []
    lines.append("# Supervised CIP Classification")
    lines.append("")
    lines.append("## Setup")
    lines.append("")
    lines.append(f"- Number of classes: {len(classes)}")
    lines.append(f"- Classes: {', '.join(classes)}")
    lines.append(f"- Evaluation: Stratified {N_SPLITS}-fold cross-validation")
    lines.append(f"- Random seed: {RANDOM_SEED}")
    lines.append("")

    test_df = metrics_df[metrics_df["split"] == "test"].copy()
    aggregate = (
        test_df.groupby("model", as_index=False)
        .agg(
            accuracy_mean=("accuracy", "mean"),
            accuracy_std=("accuracy", "std"),
            balanced_accuracy_mean=("balanced_accuracy", "mean"),
            balanced_accuracy_std=("balanced_accuracy", "std"),
            macro_f1_mean=("macro_f1", "mean"),
            macro_f1_std=("macro_f1", "std"),
        )
        .sort_values("accuracy_mean", ascending=False)
    )

    lines.append("## Test Mean ± Std Across Folds")
    lines.append("")
    lines.append("| Model | Accuracy | Balanced Accuracy | Macro F1 |")
    lines.append("|---|---:|---:|---:|")
    for row in aggregate.itertuples(index=False):
        lines.append(
            "| "
            f"{row.model} | {row.accuracy_mean:.4f} ± {row.accuracy_std:.4f} | "
            f"{row.balanced_accuracy_mean:.4f} ± {row.balanced_accuracy_std:.4f} | "
            f"{row.macro_f1_mean:.4f} ± {row.macro_f1_std:.4f} |"
        )
    lines.append("")

    lines.append("## Per-Fold Test Metrics")
    lines.append("")
    lines.append("| Model | Fold | Accuracy | Balanced Accuracy | Macro F1 |")
    lines.append("|---|---:|---:|---:|---:|")
    for row in test_df.sort_values(["model", "fold"]).itertuples(index=False):
        lines.append(
            "| "
            f"{row.model} | {row.fold} | {row.accuracy:.4f} | "
            f"{row.balanced_accuracy:.4f} | {row.macro_f1:.4f} |"
        )

    SUMMARY_FILE.write_text("\n".join(lines) + "\n")


def main() -> None:
    X, y, classes = load_dataset()
    print(
        "Loaded dataset "
        f"(n={len(y)}, dim={X.shape[1]}, classes={len(classes)})."
    )

    models = build_models()
    metrics_df = run_stratified_kfold(X, y, models)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    metrics_df.to_csv(METRICS_FILE, index=False)
    write_summary(metrics_df, classes)

    print(f"\nSaved metrics: {METRICS_FILE}")
    print(f"Saved summary: {SUMMARY_FILE}")


if __name__ == "__main__":
    main()
