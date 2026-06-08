# Build Instructions

## Repository Scope

This repository contains the final notebook, model evaluation artifacts, figures, Data Card, Model Card, Security Paper, and reproducibility instructions. The dataset file is required for execution but is not included in the repository because it is larger than GitHub's normal file-size limit.

## Prerequisites

- Python 3.10 or later, or Google Colab.
- Required dataset file: `creditcard.csv`.
- Dataset source: <https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud/data>
- Recommended Colab runtime: GPU.

## Local Setup

1. Download the dataset from Kaggle.
2. Place `creditcard.csv` in the same folder as `AISec_Final_Credit_Card_Fraud_Detection_NN_MLOps.ipynb`.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the notebook from top to bottom.
5. Confirm that the `artifacts/` folder is generated or updated.

## Colab Setup

1. Open Google Colab.
2. Upload `AISec_Final_Credit_Card_Fraud_Detection_NN_MLOps.ipynb`.
3. Upload only `creditcard.csv` into the same Colab working directory.
4. Run all cells from top to bottom.
5. Download the executed notebook and generated artifacts if you need to preserve the run outputs.

## Expected Outputs

- `artifacts/metrics_summary.csv`
- `artifacts/primary_model_metrics.json`
- `artifacts/data_quality.json`
- `artifacts/split_summary.json`
- `artifacts/run_metadata.json`
- `artifacts/security_tests.csv`
- `artifacts/slice_metrics.csv`
- `artifacts/permutation_importance.csv`
- `artifacts/local_gradient_attribution.csv`
- `artifacts/figures/`
- `artifacts/models/`

## Notes

- Do not rename the dataset file.
- Do not use another dataset path.
- The notebook reads `creditcard.csv` from the current working folder.
- Colab output metadata may show `/content/` paths because that is the Colab runtime directory.
- Use PR-AUC, recall, precision, false positives, and false negatives as the main evaluation evidence. Accuracy alone is not sufficient for this imbalanced fraud task.
