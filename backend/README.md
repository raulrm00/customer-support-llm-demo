# Backend

FastAPI backend for customer support category prediction.

## Development

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt -r backend/requirements-dev.txt
```

## Run

```powershell
cd backend
uvicorn app.main:app --reload
```

## Validation

```powershell
cd backend
black app
ruff check app
mypy app
pytest
```
