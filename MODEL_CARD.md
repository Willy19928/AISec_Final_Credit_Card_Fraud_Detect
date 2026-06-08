# Model Card: Primary NN Tabular MLP Fraud Classifier

## Model Identity

- Model name: Primary NN - Tabular MLP
- Architecture: FraudMLP(96-48-16)
- Implementation: PyTorch tabular neural network
- Runtime environment: Python 3.12.13, PyTorch 2.11.0+cu128, device `cuda`
- Model artifact: `artifacts/models/primary_mlp.pt`
- Intended use: fraud-risk scoring for credit card transactions with human review.
- Prohibited use: fully automated punishment, account blocking, or production deployment without monitoring and governance approval.

## Training Data and Features

- Dataset checksum: `76274b691b16a6c49d3f159c883398e03ccd6d1ee12d9d8ee38f4b4b98551a89`
- Training samples: 227,845
- Validation samples: 28,481
- Test samples: 28,481
- Feature count: 34
- Decision threshold selected on validation data: 0.983898

## Test Metrics

| Model | Threshold | Precision | Recall | F1-Score | ROC-AUC | PR-AUC | FP | FN | TP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Decision Tree | 0.9991 | 0.4598 | 0.8163 | 0.5882 | 0.8833 | 0.3823 | 47 | 9 | 40 |
| Random Forest | 0.8322 | 0.9070 | 0.7959 | 0.8478 | 0.9751 | 0.8654 | 4 | 10 | 39 |
| XGBoost | 0.9346 | 0.9333 | 0.8571 | 0.8936 | 0.9794 | 0.9034 | 3 | 7 | 42 |
| Isolation Forest | -0.0020 | 0.2727 | 0.3061 | 0.2885 | 0.9529 | 0.1643 | 40 | 34 | 15 |
| Primary NN - Tabular MLP | 0.9839 | 0.8478 | 0.7959 | 0.8211 | 0.9800 | 0.8267 | 7 | 10 | 39 |
| NN Autoencoder Anomaly Detector | 12.0521 | 0.5152 | 0.3469 | 0.4146 | 0.9615 | 0.4967 | 16 | 32 | 17 |

## Primary Model Decision Policy

- The model outputs a fraud probability score.
- Transactions above the selected threshold should be routed to human review.
- The threshold balances fraud recall and manual-review burden.
- Approval gate decision: **deploy with human review**.
- Approval reason: Classroom gate passed; production use would still require live monitoring and approval.

## Explainability Evidence

- Global NN explanation: `artifacts/permutation_importance.csv` and `artifacts/figures/permutation_importance.png`.
- Local NN explanation: `artifacts/local_gradient_attribution.csv` and local attribution figures.
- Top global importance features from permutation importance:

| Feature | Importance Drop |
| --- | --- |
| V14 | 0.1124 |
| V4 | 0.0487 |
| V12 | 0.0263 |
| V8 | 0.0241 |
| V10 | 0.0189 |
| V22 | 0.0129 |
| scaled_Amount | 0.0084 |
| V16 | 0.0074 |
| V3 | 0.0072 |
| V2 | 0.0051 |

## Slice and Reliability Checks

| Slice Type | Slice | Total | Fraud Count | Flag Rate | False Positive Rate | Fraud Recall |
| --- | --- | --- | --- | --- | --- | --- |
| Amount_Bin | Low | 7,126 | 26 | 0.0032 | 0.0004 | 0.7692 |
| Amount_Bin | Medium-Low | 7,115 | 3 | 0.0004 | 0.0000 | 1.0000 |
| Amount_Bin | Medium-High | 7,136 | 4 | 0.0006 | 0.0001 | 0.7500 |
| Amount_Bin | High | 7,104 | 16 | 0.0023 | 0.0004 | 0.8125 |
| Time_Bin | Night | 2,457 | 11 | 0.0045 | 0.0012 | 0.7273 |
| Time_Bin | Morning | 6,994 | 14 | 0.0023 | 0.0006 | 0.8571 |
| Time_Bin | Afternoon | 9,677 | 13 | 0.0011 | 0.0000 | 0.8462 |
| Time_Bin | Evening | 9,353 | 11 | 0.0009 | 0.0000 | 0.7273 |

## Security Stress Tests

| Model | Precision | Recall | F1-Score | PR-AUC | FP | FN | TP | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Original primary MLP test set | 0.8478 | 0.7959 | 0.8211 | 0.8267 | 7 | 10 | 39 | Original final test set. |
| PCA noise robustness std=0.03 | 0.8478 | 0.7959 | 0.8211 | 0.8265 | 7 | 10 | 39 | Adds Gaussian noise to PCA features. |
| PCA noise robustness std=0.08 | 0.8478 | 0.7959 | 0.8211 | 0.8239 | 7 | 10 | 39 | Adds Gaussian noise to PCA features. |
| Fraud amount mimicry stress test | 0.8444 | 0.7755 | 0.8085 | 0.8116 | 7 | 11 | 38 | For true fraud cases only, amount-derived features are shifted toward low-amount behavior. |
| Training-serving skew: amount features zeroed | 0.8478 | 0.7959 | 0.8211 | 0.8312 | 7 | 10 | 39 | Simulates an inference pipeline bug where amount-derived normalized features are unavailable. |

## Monitoring, Rollback, and Residual Risk

- Monitor input schema, amount distribution drift, fraud-rate drift, score distribution drift, review workload, and post-label precision/recall.
- Roll back or block deployment if recall drops materially, false positives exceed review capacity, or data quality checks fail.
- Residual risks include adaptive fraud behavior, missing demographic fairness attributes, PCA privacy limitations, and possible training-serving skew in production.
