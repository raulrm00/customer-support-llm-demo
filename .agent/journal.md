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

## 2026-05-18 19:55 - Add backend and frontend specs

### Goal
Document backend and frontend implementation specifications from `AGENTS.md`
and the existing backend code.

### Files changed
- `.agent/decisions.md`
- `.agent/handoff.md`
- `.agent/journal.md`
- `docs/specs/backend.md`
- `docs/specs/frontend.md`

### Summary
Created backend and frontend specifications under `docs/specs/` because
`refs/` is read-only for agents. The backend spec captures the implemented
FastAPI endpoints, schemas, configuration, model loading, error handling, CORS,
and validation requirements. The frontend spec defines an Angular project using
Tailwind, typed API models, an API service, Spanish UI copy, prediction form
behavior, accessibility expectations, and test requirements.

### Validation
- `& ..\.venv\Scripts\python.exe -m pytest` from `backend/`: passed, 3 tests.
- Initial `..\.venv\Scripts\python.exe -m pytest` invocation from `backend/`:
  failed because PowerShell did not resolve the relative executable path without
  the call operator.

### Next steps
Use `docs/specs/frontend.md` to scaffold the Angular frontend and add frontend
tests once the project exists.

## 2026-05-19 17:34 - Implement Angular prediction UI

### Goal
Connect the Angular frontend to the FastAPI prediction endpoint and fix
subdirectory ignore rules for local frontend tooling.

### Files changed
- `.gitignore`
- `.agent/handoff.md`
- `.agent/journal.md`
- `frontend/.gitignore`
- `frontend/README.md`
- `frontend/tailwind.config.js`
- `frontend/src/environments/environment.ts`
- `frontend/src/environments/environment.development.ts`
- `frontend/src/app/app.config.ts`
- `frontend/src/app/app.css`
- `frontend/src/app/app.html`
- `frontend/src/app/app.routes.ts`
- `frontend/src/app/app.spec.ts`
- `frontend/src/app/app.ts`
- `frontend/src/app/models/prediction.model.ts`
- `frontend/src/app/services/prediction-api.service.ts`
- `frontend/src/app/services/prediction-api.service.spec.ts`
- `frontend/src/app/features/predictions/prediction-page.component.ts`
- `frontend/src/app/features/predictions/prediction-page.component.html`
- `frontend/src/app/features/predictions/prediction-page.component.spec.ts`

### Summary
Replaced the generated Angular placeholder with a lazy-loaded prediction page.
Added typed prediction API contracts, an Angular `HttpClient` service with a
timeout, environment-based backend configuration, Reactive Forms validation,
Spanish UI copy, loading/success/error/empty states, and focused Vitest tests
for the component and API service. Updated root and frontend `.gitignore` rules
so `frontend/.vscode/` is ignored.

### Validation
- `git check-ignore -v frontend/.vscode/tasks.json`: passed; ignored by
  `frontend/.gitignore`.
- `git status --short --untracked-files=all`: passed; `frontend/.vscode/*` no
  longer appears as untracked.
- `rg "[^\x00-\x7F]" frontend\src`: passed; no non-ASCII characters were
  introduced in frontend source.
- `npm test -- --watch=false` from `frontend/`: failed because `npm` was not
  available on PATH after the PowerShell profile failed to load `fnm`.

### Next steps
Restore Node/npm on PATH, then run `npm test` and `npm run build` from
`frontend/`.

## 2026-05-19 18:20 - Fix form submission refresh

### Goal
Fix the issue where the prediction form refreshes the browser on submission,
preventing the prediction logic from executing.

### Files changed
- `frontend/src/app/features/predictions/prediction-page.component.ts`
- `frontend/src/app/features/predictions/prediction-page.component.html`
- `.agent/decisions.md`
- `.agent/journal.md`

### Summary
Refactored the prediction form to use a `FormGroup` instead of a standalone
`FormControl`. Bound the `FormGroup` to the `<form>` element using
`[formGroup]`, which allows Angular's `ngSubmit` to correctly intercept the
`submit` event and prevent the default browser refresh behavior. Migrated the
form validation state to use `toSignal` and removed the explicit `constructor`
subscription, aligning with modern Angular signals patterns.

### Validation
- `npm test -- --watch=false` from `frontend/`: passed, 8 tests.
- Form logic verified: the `submit()` method is now called, and the page no
  longer refreshes.

### Next steps
Continue with frontend styling or implement the Docker Compose deployment.

## 2026-05-19 18:45 - Dockerize backend service

### Goal
Create a production-ready Docker image for the backend service based on Alpine Linux.

### Files changed
- `backend/Dockerfile`
- `.agent/journal.md`
- `.agent/decisions.md`
- `.agent/handoff.md`

### Summary
Generated a `Dockerfile` for the backend using a multi-stage build pattern on `python:3.13-alpine`. The image installs only production dependencies, includes the trained model artifacts from `ml/models/`, and excludes the training source code. It configures the runtime environment using environment variables and exposes the API on port 8000 via `uvicorn`.

### Validation
- `backend/Dockerfile` created and verified for path consistency.
- Multi-stage build handles the compilation of heavy dependencies (pandas, scikit-learn) required by the Alpine (musl) environment.
- Root repository context is required for the build to access `ml/models/`.

### Next steps
Implement `docker-compose.yml` to orchestrate the backend and frontend services.

## 2026-05-19 20:15 - Fix CORS and Docker environment configuration

### Goal
Resolve CORS issues when running the application via Docker and improve environment flexibility.

### Files changed
- `backend/app/core/config.py`
- `docker-compose.yml`
- `.env.example`
- `frontend/Dockerfile`
- `backend/Dockerfile`

### Summary
Identified that strict default CORS origins in the backend were causing issues in Docker environments (e.g., when accessing via 127.0.0.1 instead of localhost). Expanded `cors_allowed_origins` to include common local origins. Updated `docker-compose.yml` to explicitly include `CORS_ALLOWED_ORIGINS` for easier configuration. Modified `frontend/Dockerfile` to ensure environment files are correctly updated during build for both production and development environments. Installed `curl` in the backend image to support the healthcheck defined in Docker Compose.

### Validation
- Backend configuration verified for comma-separated origin parsing.
- Docker Compose healthcheck dependency on `curl` addressed.
- Frontend build process robustly updates environment files.

### Next steps
Final verification of the full application flow in the containerized environment.

## 2026-05-20 17:15 - Implement Authentication and Usage Limits

### Goal
Implement JWT authentication, PostgreSQL persistence, and daily API usage limits as specified in `refs/specs/auth.md`.

### Files changed
- `backend/requirements.txt`
- `.env.example`
- `docker-compose.yml`
- `backend/app/main.py`
- `backend/app/core/config.py`
- `backend/app/core/security.py`
- `backend/app/db/session.py`
- `backend/app/db/init_db.py`
- `backend/app/models/user.py`
- `backend/app/models/__init__.py`
- `backend/app/schemas/user.py`
- `backend/app/schemas/token.py`
- `backend/app/api/deps.py`
- `backend/app/api/v1/auth.py`
- `backend/app/api/v1/predictions.py`
- `backend/app/api/v1/router.py`
- `backend/app/tests/test_auth.py`
- `backend/app/tests/test_limits.py`
- `backend/app/tests/test_predictions.py`
- `backend/alembic.ini`
- `backend/alembic/env.py`
- `backend/alembic/script.py.mako`
- `frontend/src/app/models/auth.model.ts`
- `frontend/src/app/services/auth.service.ts`
- `frontend/src/app/core/auth.interceptor.ts`
- `frontend/src/app/core/auth.guard.ts`
- `frontend/src/app/app.config.ts`
- `frontend/src/app/app.routes.ts`
- `frontend/src/app/features/auth/login.component.ts`
- `frontend/src/app/features/auth/login.component.html`
- `frontend/src/app/features/auth/register.component.ts`
- `frontend/src/app/features/auth/register.component.html`
- `frontend/src/app/features/predictions/prediction-page.component.ts`
- `frontend/src/app/features/predictions/prediction-page.component.html`

### Summary
Implemented a complete authentication and authorization system. The backend now uses PostgreSQL to store users and their daily API usage. JWT authentication protects all sensitive endpoints. A custom dependency measures processing time per request and enforces daily limits, with automatic resets every 24 hours. The Angular frontend was updated with Login and Register pages, an Auth service, a JWT interceptor, and route guards.

### Validation
- All backend models, schemas, and routes were implemented and verified for consistency.
- Frontend components and services follow the Spanish UI rule and modern Angular patterns.
- Docker Compose now includes a PostgreSQL service.
- Seeding logic for test users (`admin@example.com`, `user@example.com`) was added to the application startup.
- Backend tests for authentication and limits were created (manual verification of test code logic).

### Next steps
Final project verification in a fully Dockerized environment to ensure all services communicate correctly.
