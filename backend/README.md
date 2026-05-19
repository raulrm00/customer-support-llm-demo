# Backend - Customer Support Classifier API

FastAPI service for customer support category prediction using a trained scikit-learn pipeline.

## Features

- **Inference**: Predicts one of 11 support categories.
- **Health Check**: Endpoint for monitoring service status.
- **Validation**: Strict request validation using Pydantic.
- **OpenAPI**: Automatic documentation via Swagger UI.

## Requirements

- Python 3.13+
- Trained model artifact (`ml/models/modelo_idf.joblib`)

## Local Setup

1. **Create and activate virtual environment**:
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

2. **Install dependencies**:
   ```powershell
   pip install -r backend/requirements.txt -r backend/requirements-dev.txt
   ```

3. **Configure environment**:
   Create a `.env` file in the root or `backend/` directory (see `.env.example`).

## Development

Run the server with hot-reload:
```powershell
cd backend
uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`.
Documentation: `http://localhost:8000/docs`.

## Docker

### Build Image
Execute from the repository root:
```powershell
docker build -t customer-support-backend -f backend/Dockerfile .
```

### Run Container
```powershell
docker run -p 8000:8000 --env-file .env customer-support-backend
```

## Validation

Run the following commands to ensure code quality:
```powershell
cd backend
black app        # Formatting
ruff check app   # Linting
mypy app         # Type checking (if configured)
pytest           # Unit tests
```

## API Specification

- `GET /api/v1/health`: Returns service health status.
- `POST /api/v1/predictions`: Classifies a support request.

Example request:
```json
{
  "instruction": "I have an issue with my last order"
}
```
