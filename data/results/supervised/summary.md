# Supervised CIP Classification

## Setup

- Number of classes: 23
- Classes: 01, 05, 09, 11, 12, 13, 14, 15, 16, 19, 22, 26, 29, 30, 40, 42, 43, 45, 46, 47, 50, 51, 52
- Evaluation: Stratified 5-fold cross-validation
- Random seed: 42

## Test Mean ± Std Across Folds

| Model | Accuracy | Balanced Accuracy | Macro F1 |
|---|---:|---:|---:|
| logistic_regression_pca95 | 0.9249 ± 0.0207 | 0.9182 ± 0.0296 | 0.9126 ± 0.0272 |
| logistic_regression | 0.9193 ± 0.0149 | 0.9117 ± 0.0204 | 0.9067 ± 0.0172 |
| svm_rbf_pca95 | 0.9130 ± 0.0191 | 0.8960 ± 0.0318 | 0.8988 ± 0.0261 |
| svm_rbf | 0.9122 ± 0.0188 | 0.8892 ± 0.0282 | 0.8969 ± 0.0228 |
| dnn_mlp | 0.9075 ± 0.0233 | 0.8900 ± 0.0311 | 0.8881 ± 0.0297 |
| dnn_mlp_early_stopping | 0.8900 ± 0.0284 | 0.8614 ± 0.0358 | 0.8668 ± 0.0373 |

## Per-Fold Test Metrics

| Model | Fold | Accuracy | Balanced Accuracy | Macro F1 |
|---|---:|---:|---:|---:|
| dnn_mlp | 1 | 0.9170 | 0.8992 | 0.9019 |
| dnn_mlp | 2 | 0.8696 | 0.8346 | 0.8378 |
| dnn_mlp | 3 | 0.9012 | 0.9081 | 0.8847 |
| dnn_mlp | 4 | 0.9249 | 0.9044 | 0.9064 |
| dnn_mlp | 5 | 0.9246 | 0.9035 | 0.9095 |
| dnn_mlp_early_stopping | 1 | 0.9130 | 0.8951 | 0.8955 |
| dnn_mlp_early_stopping | 2 | 0.8696 | 0.8196 | 0.8279 |
| dnn_mlp_early_stopping | 3 | 0.8538 | 0.8336 | 0.8281 |
| dnn_mlp_early_stopping | 4 | 0.9209 | 0.8995 | 0.9078 |
| dnn_mlp_early_stopping | 5 | 0.8929 | 0.8590 | 0.8745 |
| logistic_regression | 1 | 0.9130 | 0.8972 | 0.8930 |
| logistic_regression | 2 | 0.9012 | 0.8833 | 0.8847 |
| logistic_regression | 3 | 0.9130 | 0.9311 | 0.9113 |
| logistic_regression | 4 | 0.9328 | 0.9232 | 0.9211 |
| logistic_regression | 5 | 0.9365 | 0.9236 | 0.9233 |
| logistic_regression_pca95 | 1 | 0.9209 | 0.9119 | 0.9020 |
| logistic_regression_pca95 | 2 | 0.8933 | 0.8724 | 0.8725 |
| logistic_regression_pca95 | 3 | 0.9249 | 0.9356 | 0.9171 |
| logistic_regression_pca95 | 4 | 0.9486 | 0.9507 | 0.9444 |
| logistic_regression_pca95 | 5 | 0.9365 | 0.9201 | 0.9273 |
| svm_rbf | 1 | 0.9130 | 0.9019 | 0.9077 |
| svm_rbf | 2 | 0.8933 | 0.8465 | 0.8698 |
| svm_rbf | 3 | 0.8933 | 0.8745 | 0.8748 |
| svm_rbf | 4 | 0.9328 | 0.9113 | 0.9156 |
| svm_rbf | 5 | 0.9286 | 0.9116 | 0.9168 |
| svm_rbf_pca95 | 1 | 0.9170 | 0.9128 | 0.9153 |
| svm_rbf_pca95 | 2 | 0.8893 | 0.8428 | 0.8608 |
| svm_rbf_pca95 | 3 | 0.8972 | 0.8904 | 0.8839 |
| svm_rbf_pca95 | 4 | 0.9289 | 0.9135 | 0.9093 |
| svm_rbf_pca95 | 5 | 0.9325 | 0.9203 | 0.9246 |
