# SDG 8 Credit Card Fraud Detection

This project builds a reproducible AI security workflow for credit card fraud detection under SDG 8. The primary model is a tabular neural network classifier, with an autoencoder anomaly detector and classical comparison models for evidence.

## Project Contents

- `AISec_Final_Credit_Card_Fraud_Detection_NN_MLOps.ipynb`: executable notebook.
- `creditcard.csv`: required local dataset file, not included in this repository because it is larger than GitHub's normal file-size limit.
- `artifacts/`: extracted Colab artifacts, including figures, metrics, cards, metadata, and model files.
- `BUILD_INSTRUCTIONS.md`: build and execution guide.
- `DATA_CARD.md`: dataset documentation.
- `MODEL_CARD.md`: primary model documentation.
- `SECURITY_PAPER.md`: final security paper.
- `requirements.txt`: Python dependency list.

## Colab Result Summary

- Dataset records: 284,807
- Fraud cases: 492
- Fraud rate: 0.1727%
- Primary model: Primary NN - Tabular MLP
- Primary PR-AUC: 0.8267
- Primary recall: 0.7959
- Primary precision: 0.8478
- Approval gate: deploy with human review

## Model Comparison

| Model | Threshold | Precision | Recall | F1-Score | ROC-AUC | PR-AUC | FP | FN | TP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Decision Tree | 0.9991 | 0.4598 | 0.8163 | 0.5882 | 0.8833 | 0.3823 | 47 | 9 | 40 |
| Random Forest | 0.8322 | 0.9070 | 0.7959 | 0.8478 | 0.9751 | 0.8654 | 4 | 10 | 39 |
| XGBoost | 0.9346 | 0.9333 | 0.8571 | 0.8936 | 0.9794 | 0.9034 | 3 | 7 | 42 |
| Isolation Forest | -0.0020 | 0.2727 | 0.3061 | 0.2885 | 0.9529 | 0.1643 | 40 | 34 | 15 |
| Primary NN - Tabular MLP | 0.9839 | 0.8478 | 0.7959 | 0.8211 | 0.9800 | 0.8267 | 7 | 10 | 39 |
| NN Autoencoder Anomaly Detector | 12.0521 | 0.5152 | 0.3469 | 0.4146 | 0.9615 | 0.4967 | 16 | 32 | 17 |

## Submission Notes

The notebook reads only `creditcard.csv` from the same working folder. The dataset can be downloaded from the Kaggle Credit Card Fraud Detection dataset page: <https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud/data>.

The returned Colab notebook and extracted `artifacts/` folder are the source of truth for final metrics and figures. Some artifact metadata may contain `/content/` paths because that is the Google Colab runtime directory; the notebook source itself does not depend on `/content/` or Google Drive paths.
