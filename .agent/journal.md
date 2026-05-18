# Agent Journal

## 2026-05-18 16:54 - Implement backend inference API

### Goal
Create the FastAPI backend described by `AGENTS.md` and align the prediction
contract with `refs/specs/ml.md` and the reference inference notebook.

### Files changed
- `.gitignore`
- `.env.example`
- `backend/README.md`
- `backend/requirements.txt`
- `backend/requirements-dev.txt`
- `backend/pyproject.toml`
- `backend/app/main.py`
- `backend/app/api/v1/health.py`
- `backend/app/api/v1/predictions.py`
- `backend/app/api/v1/router.py`
- `backend/app/core/config.py`
- `backend/app/core/errors.py`
- `backend/app/schemas/health.py`
- `backend/app/schemas/prediction.py`
- `backend/app/services/model_loader.py`
- `backend/app/services/prediction_service.py`
- `backend/app/tests/test_health.py`
- `backend/app/tests/test_predictions.py`
- `.agent/decisions.md`
- `.agent/handoff.md`

### Summary
Implemented a versioned FastAPI backend with `GET /api/v1/health` and
`POST /api/v1/predictions`. The prediction service loads a full scikit-learn
pipeline with `joblib`, passes a pandas `DataFrame` with the `instruction`
column, returns the predicted support category, and includes model and pipeline
version metadata. Added configuration via environment variables and tests for
health and prediction behavior.

### Validation
- `C:\WPy64-3.13.12.0\notebooks\CustomerSupportProject\.venv\Scripts\python.exe -m black app`: passed.
- `..\.venv\Scripts\python.exe -m ruff check app`: passed.
- `..\.venv\Scripts\python.exe -m mypy app`: passed.
- `..\.venv\Scripts\python.exe -m pytest`: passed, 3 tests.

### Next steps
Refactor the ML notebooks into production scripts under `ml/src/` and generate
the configured `ml/models/modelo_idf.joblib` artifact for real inference.

## 2026-05-18 17:14 - Implement ML training pipeline

### Goal
Refactor the reference notebook workflow into an executable ML pipeline that
trains `ml/models/modelo_idf.joblib` for backend inference.

### Files changed
- `.env.example`
- `backend/app/core/config.py`
- `ml/README.md`
- `ml/requirements.txt`
- `ml/requirements-dev.txt`
- `ml/pyproject.toml`
- `ml/params.yaml`
- `ml/dvc.yaml`
- `ml/src/schemas/customer_support.py`
- `ml/src/preprocessing/cleaning.py`
- `ml/src/evaluation/metrics.py`
- `ml/src/training/train.py`
- `ml/src/inference/predict.py`
- `ml/tests/test_training.py`
- `ml/models/modelo_idf.joblib`
- `ml/models/model_metadata.json`
- `ml/dvclive/metrics.json`
- `ml/dvclive/params.json`

### Summary
Implemented a reproducible scikit-learn training pipeline using a full
`Pipeline` with `ColumnTransformer`, `TfidfVectorizer`, and
`LogisticRegression`. The training script validates the processed dataset with
Pandera, writes model metadata, logs metrics under `dvclive/`, and persists the
production artifact as `modelo_idf.joblib`. Updated the backend default model
path to consume this artifact.

### Validation
- `..\.venv\Scripts\python.exe -m black src tests` from `ml/`: passed.
- `..\.venv\Scripts\python.exe -m ruff check src tests` from `ml/`: passed.
- `..\.venv\Scripts\python.exe -m mypy src` from `ml/`: passed.
- `..\.venv\Scripts\python.exe -m pytest` from `ml/`: passed, 1 test.
- `..\.venv\Scripts\python.exe -m src.training.train` from `ml/`: passed and generated `modelo_idf.joblib`.
- Backend real-model smoke test with `POST /api/v1/predictions`: passed, returned `ORDER`.
- Backend `black`, `ruff`, `mypy`, and `pytest`: passed, 3 tests.
- `dvc status`: failed because the workspace is not initialized as a DVC repository.
- `dvc metrics show`: failed because DVC could not trust the repository owner in this environment.

### Next steps
Initialize/configure DVC ownership for the workspace, then run `dvc status`,
`dvc repro`, and `dvc metrics show` through the DVC-managed pipeline.

## 2026-05-18 18:02 - Initialize DVC training pipeline

### Goal
Initialize DVC and remove the ML training dependency on `refs/`.

### Files changed
- `.dvc/config`
- `.dvc/.gitignore`
- `.dvcignore`
- `.gitignore`
- `.agent/decisions.md`
- `.agent/handoff.md`
- `.agent/journal.md`
- `ml/README.md`
- `ml/data/raw/bitext-limpio.parquet.dvc`
- `ml/dvc.lock`
- `ml/dvc.yaml`
- `ml/models/.gitignore`
- `ml/params.yaml`
- `ml/tests/test_dvc_configuration.py`

### Summary
Initialized DVC for the repository, copied the Bitext parquet dataset from
`refs/data/` to `ml/data/raw/`, and tracked the ML copy with DVC. Updated
`params.yaml` and `dvc.yaml` so training uses the DVC-managed ML dataset, not
`refs/`. Added Git/DVC ignores for `refs/` and local caches, made
`model_metadata.json` a generated DVC output, generated `ml/dvc.lock`, and added
tests that prevent the default training configuration from pointing back to
`refs/`.

### Validation
- `.\.venv\Scripts\python.exe -m dvc add ml\data\raw\bitext-limpio.parquet`: passed.
- `.\.venv\Scripts\python.exe -m dvc repro ml\dvc.yaml`: passed and regenerated the model, metadata, metrics, and lock file.
- `.\.venv\Scripts\python.exe -m dvc status`: passed, data and pipelines are up to date.
- `.\.venv\Scripts\python.exe -m dvc metrics show`: passed, reported train/validation/test metrics.
- `..\.venv\Scripts\python.exe -m black src tests` from `ml/`: passed.
- `..\.venv\Scripts\python.exe -m ruff check src tests` from `ml/`: passed.
- `..\.venv\Scripts\python.exe -m mypy src` from `ml/`: passed.
- `..\.venv\Scripts\python.exe -m pytest` from `ml/`: passed, 3 tests with 1 DVCLive dependency warning.
- `..\.venv\Scripts\python.exe -m pytest` from `backend/`: passed, 3 tests.

### Next steps
Configure a DVC remote and run `dvc push` so the dataset and generated model
artifacts are available outside the local cache.
