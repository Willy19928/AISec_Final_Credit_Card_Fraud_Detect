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
3. Verify the dataset checksum:

```powershell
Get-FileHash .\creditcard.csv -Algorithm SHA256
```

Expected SHA-256:

```text
76274b691b16a6c49d3f159c883398e03ccd6d1ee12d9d8ee38f4b4b98551a89
```

If the checksum does not match, stop and download the dataset again before
running the notebook. A different checksum means the generated evidence will
not match the documented final run.

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Run the notebook from top to bottom.
6. Confirm that the `artifacts/` folder is generated or updated.

## Colab Setup

1. Open Google Colab.
2. Upload `AISec_Final_Credit_Card_Fraud_Detection_NN_MLOps.ipynb`.
3. Upload only `creditcard.csv` into the same Colab working directory.
4. Run all cells from top to bottom.
5. Download the executed notebook and generated artifacts if you need to preserve the run outputs.

## Expected Outputs

- `DATA_CARD.md`
- `MODEL_CARD.md`
- `artifacts/metrics_summary.csv`
- `artifacts/primary_model_metrics.json`
- `artifacts/data_quality.json`
- `artifacts/split_summary.json`
- `artifacts/run_metadata.json`
- `artifacts/security_tests.csv`
- `artifacts/slice_metrics.csv`
- `artifacts/permutation_importance.csv`
- `artifacts/local_gradient_attribution.csv`
- `artifacts/artifact_manifest.csv`
- `artifacts/DATA_CARD.md`
- `artifacts/MODEL_CARD.md`
- `artifacts/autoencoder_training_history.csv`
- `artifacts/mlp_training_history.csv`
- `artifacts/figures/class_distribution.png`
- `artifacts/figures/confusion_matrices_and_roc.png`
- `artifacts/figures/eda_summary.png`
- `artifacts/figures/local_attribution_fraud_case.png`
- `artifacts/figures/local_attribution_normal_case.png`
- `artifacts/figures/pca_feature_distributions.png`
- `artifacts/figures/permutation_importance.png`
- `artifacts/figures/precision_recall_curves.png`
- `artifacts/figures/primary_mlp_threshold_tuning.png`
- `artifacts/figures/security_stress_tests.png`
- `artifacts/figures/slice_checks.png`
- `artifacts/figures/xgboost_feature_importance.png`
- `artifacts/models/autoencoder.pt`
- `artifacts/models/comparison_models.joblib`
- `artifacts/models/preprocessing.joblib`
- `artifacts/models/primary_mlp.pt`
- `AISec_Final_Artifacts.zip`

The artifact manifest records each artifact's file size and SHA-256 hash. Text
artifact hashes use LF-normalized bytes so verification is stable across Windows
and Linux checkouts; binary artifact hashes use their exact bytes. Run the
verifier after regenerating artifacts:

```bash
python scripts/verify_artifact_manifest.py
```

## Deploy The Primary Model

The deployment implementation is maintained separately at
[Willy19928/Credit_Card_Fraud_Detection_Server](https://github.com/Willy19928/Credit_Card_Fraud_Detection_Server).

After running the notebook, copy these generated artifacts into the server
repository's `models/` directory:

```text
artifacts/models/primary_mlp.pt        -> models/primary_mlp.pt
artifacts/models/preprocessing.joblib  -> models/preprocessing.joblib
artifacts/run_metadata.json            -> models/run_metadata.json
```

The checkpoint and preprocessing artifact must come from the same notebook run.
The server validates the MLP architecture, feature-column order, fitted scaler
behavior, threshold, finite model parameters, run metadata, and artifact hashes
at startup. After copying the files, regenerate the deployment server manifest
so the startup hash checks match the new artifacts:

```powershell
$TrainingRepo = (Get-Location).Path
cd ..
git clone https://github.com/Willy19928/Credit_Card_Fraud_Detection_Server.git
cd Credit_Card_Fraud_Detection_Server

Copy-Item "$TrainingRepo\artifacts\models\primary_mlp.pt" .\models\primary_mlp.pt -Force
Copy-Item "$TrainingRepo\artifacts\models\preprocessing.joblib" .\models\preprocessing.joblib -Force
Copy-Item "$TrainingRepo\artifacts\run_metadata.json" .\models\run_metadata.json -Force
python .\scripts\update_model_manifest.py
```

Start the deployment server with Docker:

```bash
docker compose up -d --build
```

Open `http://localhost` for the browser review console. See
`DEPLOYMENT_SERVER.md` for the input schema, API endpoints, and Azure VM
deployment relationship.

## Notes

- Do not rename the dataset file.
- Do not use another dataset path.
- The notebook reads `creditcard.csv` from the current working folder.
- The notebook clears and regenerates `artifacts/` at the start of a full run so obsolete files are not carried into the final manifest or zip package.
- Colab output metadata may show `/content/` paths because that is the Colab runtime directory.
- Use PR-AUC, recall, precision, false positives, and false negatives as the main evaluation evidence. Accuracy alone is not sufficient for this imbalanced fraud task.
