# Handoff

## Current implementation phase
Initial backend, ML training, and DVC pipeline implementation.

## Main working areas
- FastAPI backend under `backend/`.
- Customer support category prediction using `ml/models/modelo_idf.joblib`.
- ML training scripts under `ml/src/`.
- DVC-managed ML dataset at `ml/data/raw/bitext-limpio.parquet`.
- DVC training stage in `ml/dvc.yaml`.
- Backend and frontend implementation specifications under `docs/specs/`.

## Known blockers
- No current DVC blocker. DVC commands required elevated execution in this
  environment because the sandbox could not access DVC/Git cache files.

## Commands needed to run the project
```powershell
cd backend
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

```powershell
cd ml
..\.venv\Scripts\python.exe -m src.training.train
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
Scaffold the Angular frontend with Tailwind using `docs/specs/frontend.md`, or
configure a DVC remote for team storage and run `dvc push`.
