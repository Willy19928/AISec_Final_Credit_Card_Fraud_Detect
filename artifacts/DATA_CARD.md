# Data Card: Credit Card Fraud Detection Dataset

## Dataset Identity

- Dataset file used by this project: `creditcard.csv`
- Source identity: public credit card fraud detection dataset from the ULB Machine Learning Group / Worldline research collaboration.
- Source URL: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud/data
- License: Database: Open Database; Contents: Database Contents
- Original context: European cardholder transactions from September 2013 over a two-day period.
- Project task: binary fraud detection for SDG 8 financial security and trustworthy economic activity.
- Target label: `Class`, where `1` means fraudulent transaction and `0` means normal transaction.
- Checksum from Colab run: `76274b691b16a6c49d3f159c883398e03ccd6d1ee12d9d8ee38f4b4b98551a89`

## Dataset Summary

- Records: 284,807
- Columns: 31
- Normal transactions: 284,315
- Fraud transactions: 492
- Fraud rate: 0.1727%
- Missing values: 0
- Duplicate rows detected: 1,081

## Schema and Features

- Original columns: `Time`, `Amount`, anonymized PCA features `V1` to `V28`, and `Class`.
- Engineered features: `Hour`, `Hour_sin`, `Hour_cos`, `scaled_Time`, `scaled_Amount`, and `scaled_log_Amount`.
- Final feature count: 34
- Final feature list: V1, V2, V3, V4, V5, V6, V7, V8, V9, V10, V11, V12, V13, V14, V15, V16, V17, V18, V19, V20, V21, V22, V23, V24, V25, V26, V27, V28, Hour, Hour_sin, Hour_cos, scaled_Time, scaled_Amount, scaled_log_Amount

## Processing Lineage

- The notebook loads one local CSV file named `creditcard.csv`.
- The split is stratified into train, validation, and test sets.
- Training samples: 227,845; fraud: 394
- Validation samples: 28,481; fraud: 49
- Test samples: 28,481; fraud: 49
- Scaling is fitted on the training split only and then applied to validation and test data.
- SMOTE is applied only to the training split for classical comparison models.
- Neural-network training uses imbalance-aware sampling without changing validation or test labels.

## Quality, Fairness, and Privacy Limits

- The dataset is extremely imbalanced, so PR-AUC, recall, precision, and error counts are more meaningful than accuracy alone.
- The dataset does not include demographic attributes. Direct demographic fairness cannot be measured.
- Amount-bin and time-window slice checks are used as proxy reliability checks, not demographic fairness claims.
- PCA-anonymized features reduce exposure of raw transaction attributes, but they do not guarantee complete privacy.

## Security Controls

- Dataset checksum is recorded for tamper checking.
- Data quality, split metadata, artifact manifest, and stress-test outputs are generated at runtime.
- Production use would still require access control, data retention controls, poisoning monitoring, and incident response.
