# Handoff

## Current implementation phase
Auth System & Usage Limits Integration.

## Main working areas
- FastAPI backend under `backend/`.
- ML training and DVC pipeline under `ml/`.
- Angular prediction UI under `frontend/`.
- JWT Authentication and PostgreSQL persistence.
- Daily usage limits and automatic reset logic.
- Dockerization of all services (Backend, Frontend, DB).
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
- `DATABASE_URL`: connection string for PostgreSQL
- `JWT_SECRET_KEY`: secret for token signing
- `DEFAULT_DAILY_LIMIT_SECONDS`: default limit for new users
- `MODEL_ARTIFACT_PATH`: path to model artifact
- `API_BASE_URL`: (Frontend build arg) URL for the backend API

## Known risks
- `ml/models/model_metadata.json` is a generated DVC output.
- DVC remote not yet configured for team-wide artifact sharing.
- Multi-stage Docker build handles Alpine (musl) compatibility, but some specific binary packages might need tuning if dependencies change.
- Database migrations must be managed with Alembic for production schema updates.

## Suggested next task
Final manual verification of the login/register/prediction flow with a focus on edge cases (e.g., token expiration, limit reached).
