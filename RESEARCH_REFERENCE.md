# Research Reference: SecMLOps

## Selected Paper

This project cites the following paper as a reference for explaining and
checking the security-related MLOps practices used in the project:

> Xinrui Zhang, Pincan Zhao, Jason Jaskolka, Heng Li, and Rongxing Lu.
> "SecMLOps: A comprehensive framework for integrating security throughout the
> machine learning operations lifecycle." *Empirical Software Engineering*,
> volume 31, article 74, 2026.
> <https://doi.org/10.1007/s10664-025-10795-y>

The paper presents SecMLOps as a security-first extension of MLOps. In this
project, it is used as supporting literature for discussing provenance, artifact
integrity, validation, controlled deployment, security testing, and limitations.
The fraud-detection task, model selection, dataset, and deployment demo are not
derived from the paper.

## Relevant Reference Ideas

The reference ideas most relevant to this project are:

- the People, Technology, Processes, Governance, and Compliance (PTPGC)
  perspective for treating ML security as more than a model-only problem;
- lifecycle-specific threat analysis, including data poisoning, adversarial
  inputs, model extraction, tampering, repudiation, and drift exploitation;
- provenance tracking for datasets, feature transformations, training runs, and
  model artifacts;
- Data Cards, Model Cards, automated CI/CD checks, input validation, checksums,
  security testing, and controlled model deployment;
- multi-layered defenses and explicit evaluation of security-performance
  trade-offs;
- continuous monitoring, rollback, and incident response as requirements for a
  production ML system.

## How This Project Uses The Reference

This repository and the deployment repository already implement a limited,
classroom-scale set of MLSecOps/SecMLOps-style practices. The paper is used to
describe how those existing practices relate to common SecMLOps concepts; it is
not the source of the fraud-detection project design.

| Reference concept | Existing project practice | Evidence |
| --- | --- | --- |
| Security across the ML lifecycle | Training evidence and deployment behavior are maintained in separate, linked repositories. Security limits are documented from dataset loading through serving. | `SECURITY_PAPER.md`, `DEPLOYMENT_SERVER.md` |
| Dataset and model provenance | The notebook enforces the dataset SHA-256, records split and run metadata, hashes generated artifacts, and gives the deployed model an artifact set ID. | `artifacts/data_quality.json`, `artifacts/run_metadata.json`, `artifacts/artifact_manifest.csv` |
| Data Card and Model Card | The notebook generates auditable documentation for the dataset, model, intended use, metrics, limitations, and deployment boundary. | `DATA_CARD.md`, `MODEL_CARD.md` |
| Automated security checks in CI/CD | Training CI verifies the artifact manifest allowlist, notebook JSON parsing, and root/artifact card sync. Server CI audits dependencies, regenerates its deployment manifest, runs API and artifact-validation tests, builds Docker, and exercises the Docker entrypoint. | `.github/workflows/artifact-integrity.yml`, deployment-server `server-ci.yml` |
| Input validation and sanitization | The notebook validates dataset identity and schema. The server rejects malformed, missing, unknown, non-finite, negative, and extreme transaction values. | Notebook data-loading checks, deployment-server `app.py` |
| Checksums for integrity | SHA-256 values detect unauthorized or accidental changes to the dataset and deployment artifacts. | Artifact manifests and server startup verification |
| Security-performance trade-off evaluation | The project reports fraud-detection metrics, slice checks, limited security stress tests, and a classroom approval gate instead of claiming security from accuracy alone. | `artifacts/security_tests.csv`, `artifacts/slice_metrics.csv`, `MODEL_CARD.md` |
| Controlled deployment | The server has no live model-upload endpoint. Model artifacts are replaced offline before startup and checked before serving. | `DEPLOYMENT_SERVER.md`, deployment-server README |

The notebook also uses early stopping for the primary neural network. The paper
discusses early stopping together with adversarial training as one defense
component. In this project, early stopping is used for validation-based model
selection and overfitting control; it has not been validated here as a defense
against data poisoning.

The project's PCA-noise, fraud-amount-mimicry, and training-serving-skew tests
match the reference paper's broader recommendation to evaluate multiple threat
scenarios and security-performance trade-offs. They do not reproduce the paper's
pedestrian-detection experiments, data-poisoning attack, FGSM attack, DeepFool
attack, adversarial training, CutMix, or model-distillation results.

## Scope Boundary

This project does **not** claim to implement the complete SecMLOps framework.
In particular, the classroom implementation does not provide:

- a full organizational PTPGC role structure;
- a complete STRIDE threat matrix or full CIAAAA control program;
- adversarial training or poisoning-resistant retraining;
- production authentication, authorization, TLS, rate limiting, or audit logs;
- continuous drift monitoring, automated rollback, or incident response.

These remain production requirements. The paper is used only as a reference for
explaining the implemented controls and documenting the limitations of controls
that are not implemented.
