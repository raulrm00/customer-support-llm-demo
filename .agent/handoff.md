# Handoff

## Current implementation phase
Initial backend and ML training implementation.

## Main working areas
- FastAPI backend under `backend/`.
- Customer support category prediction using `ml/models/modelo_idf.joblib`.
- ML training scripts under `ml/src/`.

## Known blockers
- DVC is not initialized/trusted in the current environment, so `dvc status` and
  `dvc metrics show` did not complete.

## Commands needed to run the project
```powershell
cd backend
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

```powershell
cd ml
..\.venv\Scripts\python.exe -m src.training.train
```

## Commands needed to run tests
```powershell
cd backend
pytest
```

```powershell
cd ml
pytest
```

## Static analysis commands
```powershell
cd backend
black app
ruff check app
mypy app
```

```powershell
cd ml
black src tests
ruff check src tests
mypy src
```

## Important environment variables
- `APP_ENV`
- `APP_NAME`
- `API_VERSION`
- `CORS_ALLOWED_ORIGINS`
- `MODEL_ARTIFACT_PATH`
- `MODEL_METADATA_PATH`
- `MODEL_VERSION`
- `PIPELINE_VERSION`
- `LOG_LEVEL`

## Known risks
- The prediction endpoint depends on `modelo_idf.joblib` accepting a pandas
  `DataFrame` with an `instruction` column.
- Confidence is omitted when the loaded pipeline does not support
  `predict_proba`.
- DVC commands need repository initialization and/or safe-directory ownership
  configuration before they can be used reliably in this environment.

## Suggested next task
Initialize DVC for the repository and run the ML pipeline through `dvc repro`.
