# Deployment Server Integration

## Repository Relationship

The model-training and evidence repository is:

- [Willy19928/AISec_Final_Credit_Card_Fraud_Detect](https://github.com/Willy19928/AISec_Final_Credit_Card_Fraud_Detect)

The reference inference and Azure deployment repository is:

- [Willy19928/Credit_Card_Fraud_Detection_Server](https://github.com/Willy19928/Credit_Card_Fraud_Detection_Server)

The deployment server was forked from
[joe50304/azure_cloud_inference](https://github.com/joe50304/azure_cloud_inference)
and modified from a MobileNet image-classification service into a credit-card
fraud transaction scoring service.

This repository remains the source of truth for training, evaluation metrics,
security tests, cards, and generated model artifacts. The deployment repository
is the serving implementation.

## Artifact Flow

Running the notebook generates the artifacts required by the server:

| Training repository artifact | Deployment repository destination | Purpose |
| --- | --- | --- |
| `artifacts/models/primary_mlp.pt` | `models/primary_mlp.pt` | MLP state dictionary, feature order, architecture, and decision threshold |
| `artifacts/models/preprocessing.joblib` | `models/preprocessing.joblib` | Training-fitted scalers and final feature-column order |

The two files must come from the same notebook run. Deploying a new model
without its matching preprocessing artifact can cause training-serving skew.

## Serving Input Contract

The inference API accepts exactly 30 raw numeric transaction fields:

```text
Time, V1, V2, ... V28, Amount
```

The server uses `preprocessing.joblib` to reproduce the notebook's runtime
features:

```text
V1 ... V28, Hour, Hour_sin, Hour_cos,
scaled_Time, scaled_Amount, scaled_log_Amount
```

The API rejects missing fields, unknown fields, non-numeric values, non-finite
values, negative `Time`, and negative `Amount`.

## Decision Policy

- Model architecture: `FraudMLP(96-48-16)`
- Packaged decision threshold: `0.9838983416557312`
- Score below threshold: normal flow
- Score at or above threshold: human review

The deployment server does not automatically block accounts or punish
customers.

## Server Capabilities

- Browser-based single-transaction review console.
- Normal and fraud example transactions.
- JSON batch inference.
- Compatible `.pt` model upload.
- Checkpoint validation before atomic model replacement.
- Persistent uploaded model storage through a Docker volume.
- Flask API served through Gunicorn.
- Docker and Azure VM deployment instructions.

Uploaded checkpoints must:

- use the `.pt` extension;
- contain a `FraudMLP(96-48-16)` state dictionary;
- use the same 34 model features and feature order as `preprocessing.joblib`;
- include a finite threshold between `0` and `1`;
- contain only finite model parameters.

The deployment server intentionally does not allow users to upload
`preprocessing.joblib`, because loading an untrusted joblib artifact can execute
arbitrary code.

## API Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/` | Browser fraud review console |
| `GET` | `/model_status` | Loaded model, architecture, threshold, device, and artifact hash |
| `GET` | `/schema` | Required input columns, samples, and batch limit |
| `POST` | `/predict` | Single-transaction or batch JSON inference |
| `POST` | `/upload_model` | Upload and activate a compatible `.pt` checkpoint |

Example prediction response:

```json
{
  "success": true,
  "count": 1,
  "predictions": [
    {
      "index": 0,
      "prediction": "normal",
      "fraud_probability": 0.05713778,
      "fraud_probability_percent": 5.7138,
      "threshold": 0.9838983416557312,
      "requires_human_review": false
    }
  ]
}
```

## Start The Server

```bash
git clone https://github.com/Willy19928/Credit_Card_Fraud_Detection_Server.git
cd Credit_Card_Fraud_Detection_Server
docker compose up -d --build
```

Open `http://localhost`.

For Azure VM deployment, security configuration, environment variables, and
complete API examples, follow the deployment repository's README.

## Deployment Security Boundary

The reference server is suitable for classroom demonstration and controlled
testing. A production deployment still requires:

- authentication and authorization;
- TLS termination;
- rate limiting and request-size enforcement;
- audit logging and monitoring;
- input, score, and review-workload drift monitoring;
- rollback and incident-response procedures;
- protection of transaction data and model artifacts.
