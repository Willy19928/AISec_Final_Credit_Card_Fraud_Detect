# Security Paper: SDG 8 Credit Card Fraud Detection with Neural Networks and MLSecOps

## Abstract

This project studies credit card fraud detection as an SDG 8 problem because fraudulent financial transactions harm trustworthy economic activity and create direct loss for consumers, merchants, and financial institutions. The final workflow uses a neural-network primary classifier, a neural-network autoencoder anomaly detector, and several comparison models. The work emphasizes reproducible execution, model cards, data cards, explainability, slice reliability checks, and limited AI security stress tests.

## Reference Paper and Related Method

This project references Zhang et al.'s 2026 paper, "SecMLOps: A comprehensive
framework for integrating security throughout the machine learning operations
lifecycle," as supporting literature for the MLSecOps discussion. The paper
presents SecMLOps as a security-first extension of MLOps based on People,
Technology, Processes, Governance, and Compliance (PTPGC). It recommends
lifecycle-specific threat analysis, provenance tracking, automated pipeline
checks, layered defenses, controlled deployment, continuous monitoring, and
explicit evaluation of the trade-off between security and operational
performance.

The paper is not the basis for the fraud-detection task, dataset, model choice,
or deployment demo. Instead, it is used to relate the project's existing controls
to SecMLOps concepts. Dataset checksum and schema enforcement address
data-integrity risk before training. Run metadata, artifact SHA-256 values, an
artifact set ID, Data Card, and Model Card provide provenance and auditable
evidence. CI verifies committed artifacts, while the deployment service performs
input validation, verifies model artifact hashes, rejects live model uploads,
and reports the served artifact version. The notebook's slice checks and
limited stress tests evaluate model behavior under several conditions rather
than relying only on normal test accuracy.

This is a contextual application, not a reproduction of the paper's pedestrian
detection case study. The project does not implement the paper's complete PTPGC
role structure, full STRIDE and CIAAAA analysis, data-poisoning experiment,
FGSM or DeepFool attacks, adversarial training, CutMix, model distillation,
continuous monitoring, or incident-response system. The precise mapping and
scope limits are documented in `RESEARCH_REFERENCE.md`.

## Problem and SDG 8 Motivation

The goal is to identify fraudulent credit card transactions while keeping unnecessary manual review low. The dataset is highly imbalanced: 492 fraud cases among 284,807 records, or 0.1727%. This makes accuracy misleading. A secure fraud model should improve detection, support human review, and avoid making ungoverned automated decisions.

## Dataset and Processing

The project uses one local dataset file, `creditcard.csv`, with checksum `76274b691b16a6c49d3f159c883398e03ccd6d1ee12d9d8ee38f4b4b98551a89`. The dataset source is the public ULB Machine Learning Group / Worldline credit card fraud dataset on Kaggle, licensed as `Database: Open Database; Contents: Database Contents`. It contains European cardholder transactions from September 2013 over a two-day period. The dataset has no missing values and contains 1,081 duplicate rows. Features include `Time`, `Amount`, anonymized PCA features `V1` to `V28`, and target label `Class`.

Processing uses stratified random train, validation, and test splits. The test set contains 28,481 transactions and 49 fraud cases. Scaling is fitted only on training data to reduce leakage risk. SMOTE is used only for classical comparison models, while the primary neural network uses imbalance-aware sampling. The dataset covers a two-day sequence, but this classroom run does not include temporal future-time validation, so future deployment performance may differ from the random holdout estimate.

## Model Design

The primary model is a PyTorch tabular MLP, `FraudMLP(96-48-16)`, trained as a binary fraud classifier. The project also includes a neural-network autoencoder anomaly detector and classical comparison models: Decision Tree, Random Forest, XGBoost, and Isolation Forest.

XGBoost is the strongest comparison model in the Colab run, with PR-AUC 0.9034. The primary neural network achieves PR-AUC 0.8267, recall 0.7959, precision 0.8478, and F1-score 0.8211. The final decision gate approves the primary model for human review, not fully automated action.

## Evaluation Results

| Model | Threshold | Precision | Recall | F1-Score | ROC-AUC | PR-AUC | FP | FN | TP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Decision Tree | 0.9991 | 0.4598 | 0.8163 | 0.5882 | 0.8833 | 0.3823 | 47 | 9 | 40 |
| Random Forest | 0.8322 | 0.9070 | 0.7959 | 0.8478 | 0.9751 | 0.8654 | 4 | 10 | 39 |
| XGBoost | 0.9346 | 0.9333 | 0.8571 | 0.8936 | 0.9794 | 0.9034 | 3 | 7 | 42 |
| Isolation Forest | -0.0020 | 0.2727 | 0.3061 | 0.2885 | 0.9529 | 0.1643 | 40 | 34 | 15 |
| Primary NN - Tabular MLP | 0.9839 | 0.8478 | 0.7959 | 0.8211 | 0.9800 | 0.8267 | 7 | 10 | 39 |
| NN Autoencoder Anomaly Detector | 12.0521 | 0.5152 | 0.3469 | 0.4146 | 0.9615 | 0.4967 | 16 | 32 | 17 |

## Explainability and Slice Reliability

The project uses permutation importance for global neural-network explanation and gradient-based local attribution for selected transactions. The permutation-importance subset uses 5,000 test rows: all 49 available fraud cases plus sampled normal cases. Its fraud rate is 0.98%, and its base PR-AUC is 0.9234, so it should not be compared directly with the original test-set PR-AUC under the original prevalence. The strongest global signal is `V14`, with importance drop 0.1124. The dataset does not contain demographic attributes, so demographic fairness cannot be measured directly. Instead, amount-bin and time-window slices are used as proxy reliability checks.

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

## Threat Model

The protected assets are the fraud model, transaction scoring pipeline, dataset integrity, model artifacts, and human-review workflow. Relevant adversaries include fraudsters attempting evasion, insiders or compromised accounts modifying training data, and external attackers probing a deployed scoring API. The main security goals are data integrity, robust fraud recall, controlled false positives, traceable model artifacts, and monitored deployment.

## Security and Safety Tests

The notebook implements three practical stress-test categories: PCA feature noise, fraud amount mimicry, and training-serving skew. PCA noise simulates small perturbations to anonymized transaction features. Fraud amount mimicry shifts true fraud amount-derived features toward low-amount behavior. Training-serving skew simulates an inference bug where amount-derived normalized features are missing. These tests are useful classroom evidence, but they do not fully test data poisoning, model extraction, account compromise, rate-limit abuse, or every adaptive fraud strategy in the threat model.

| Model | Precision | Recall | F1-Score | PR-AUC | FP | FN | TP | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Original primary MLP test set | 0.8478 | 0.7959 | 0.8211 | 0.8267 | 7 | 10 | 39 | Original final test set. |
| PCA noise robustness std=0.03 | 0.8478 | 0.7959 | 0.8211 | 0.8265 | 7 | 10 | 39 | Adds Gaussian noise to PCA features. |
| PCA noise robustness std=0.08 | 0.8478 | 0.7959 | 0.8211 | 0.8239 | 7 | 10 | 39 | Adds Gaussian noise to PCA features. |
| Fraud amount mimicry stress test | 0.8444 | 0.7755 | 0.8085 | 0.8116 | 7 | 11 | 38 | For true fraud cases only, amount-derived features are shifted toward low-amount behavior. |
| Training-serving skew: amount features zeroed | 0.8478 | 0.7959 | 0.8211 | 0.8312 | 7 | 10 | 39 | Simulates an inference pipeline bug where amount-derived normalized features are unavailable. |

The amount mimicry test reduces primary recall from 0.7959 to 0.7755. This shows that behavioral mimicry remains a meaningful residual risk, even when the model passes the classroom approval gate.

## MLSecOps Workflow

The workflow records dataset checksum, split metadata, training metrics, model files, explainability outputs, slice checks, security-test results, run metadata, and an artifact manifest with size and SHA-256 values. The artifact package includes model files under `artifacts/models/`, figures under `artifacts/figures/`, and structured CSV/JSON evidence for review. The deployment metadata includes an artifact set ID so the inference server can report which trained artifact bundle is being served.

The approval gate for this Colab run is **deploy with human review**. The decision is limited to human-review deployment because production use would still require live monitoring, API controls, review capacity management, incident response, rollback plans, and retraining triggers.

## Residual Risk and Remediation

Residual risks remain. Fraudsters may adapt to mimic normal behavior. PCA-anonymized features limit business interpretability and do not guarantee complete privacy. The dataset has no demographic attributes, so demographic fairness cannot be proven. The evaluation uses a random holdout rather than temporal validation. A production system would need monitoring for data drift, score drift, label delay, review workload, model extraction attempts, and data poisoning.

Recommended remediation includes human review for flagged transactions, rate limiting for scoring APIs, model artifact versioning, checksum validation for datasets, drift monitoring, scheduled post-label evaluation, rollback criteria, and periodic retraining when new fraud patterns appear.

## Conclusion

The final workflow satisfies the SDG 8 fraud-detection objective with a neural-network primary implementation, MLOps evidence, explainability, slice reliability checks, and security stress tests. The model is suitable for a classroom human-review scenario, while full production use would require stronger operational governance and continuous monitoring.

## References

- Credit Card Fraud Detection dataset: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud/data
- Dataset license: Database: Open Database; Contents: Database Contents
- Zhang X, Zhao P, Jaskolka J, Li H, Lu R (2026) SecMLOps: A comprehensive framework for integrating security throughout the machine learning operations lifecycle. *Empirical Software Engineering* 31:74. https://doi.org/10.1007/s10664-025-10795-y
