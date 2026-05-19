# Handoff

## Current implementation phase
Initial backend, ML training, DVC pipeline, and Angular prediction UI implementation.

## Main working areas
- FastAPI backend under `backend/`.
- Customer support category prediction using `ml/models/modelo_idf.joblib`.
- ML training scripts under `ml/src/`.
- DVC-managed ML dataset at `ml/data/raw/bitext-limpio.parquet`.
- DVC training stage in `ml/dvc.yaml`.
- Backend and frontend implementation specifications under `docs/specs/`.
- Angular prediction feature under `frontend/src/app/features/predictions/`.
- Backend Dockerization with `backend/Dockerfile`.

## Known blockers
- No current DVC blocker. DVC commands required elevated execution in this
  environment because the sandbox could not access DVC/Git cache files.
- Docker commands cannot be executed directly within this environment; the `Dockerfile` was verified manually.

## Commands needed to run the project
```powershell
# Build and run backend container (from repository root)
docker build -t customer-support-backend -f backend/Dockerfile .
docker run -p 8000:8000 customer-support-backend
```
```powershell
cd backend
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

```powershell
cd ml
..\.venv\Scripts\python.exe -m src.training.train
```

```powershell
cd frontend
npm start
```

```powershell
..\.venv\Scripts\python.exe -m dvc repro ml\dvc.yaml
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

```powershell
cd ml
..\.venv\Scripts\python.exe -m dvc status
..\.venv\Scripts\python.exe -m dvc metrics show
```

```powershell
cd frontend
npm test
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
- DVC has no remote configured yet, so cached data and model artifacts are local
  until a remote is added and `dvc push` is run.
- `ml/models/model_metadata.json` is now a generated DVC output, not a
  directly Git-tracked file.

## Suggested next task
Configure a DVC remote for team storage and run `dvc push`, or implement the
Docker Compose configuration for full-stack deployment.
