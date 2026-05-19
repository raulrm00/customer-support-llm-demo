# Handoff

## Current implementation phase
Deployment & Documentation.

## Main working areas
- FastAPI backend under `backend/`.
- ML training and DVC pipeline under `ml/`.
- Angular prediction UI under `frontend/`.
- Dockerization of both services.
- Orchestration with `docker-compose.yml`.
- Comprehensive documentation in root and subdirectories.

## Known blockers
- Docker commands cannot be executed directly within this environment; configuration files were verified manually.
- DVC commands may require elevated execution to access cache files.

## Commands needed to run the project
```powershell
# Recommended: Run the entire stack with Docker Compose
docker compose up --build
```

```powershell
# Backend (Manual)
cd backend
uvicorn app.main:app --reload
```

```powershell
# Frontend (Manual)
cd frontend
npm start
```

```powershell
# ML Training (Manual)
cd ml
dvc repro
```

## Commands needed to run tests
```powershell
cd backend
pytest

cd ml
pytest

cd frontend
npm test
```

## Static analysis commands
```powershell
# Backend
cd backend
black app && ruff check app

# ML
cd ml
black src tests && ruff check src tests
```

## Important environment variables
- `APP_ENV`: local/production
- `CORS_ALLOWED_ORIGINS`: allowed frontend origins
- `MODEL_ARTIFACT_PATH`: path to model artifact
- `API_BASE_URL`: (Frontend build arg) URL for the backend API

## Known risks
- `ml/models/model_metadata.json` is a generated DVC output.
- DVC remote not yet configured for team-wide artifact sharing.
- Multi-stage Docker build handles Alpine (musl) compatibility, but some specific binary packages might need tuning if dependencies change.

## Suggested next task
Final project review and verification of all components working together in a fresh environment.
