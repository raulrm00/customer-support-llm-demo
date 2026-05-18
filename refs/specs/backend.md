# Backend Specification

## Purpose

The backend is a FastAPI service for customer support categorical prediction.
It exposes versioned HTTP endpoints, loads a persisted scikit-learn pipeline,
validates requests with Pydantic, and returns safe prediction responses for an
Angular frontend.

## Runtime Stack

- Python 3.13.
- FastAPI for HTTP routing and OpenAPI generation.
- Pydantic and pydantic-settings for schemas and configuration.
- pandas for inference input framing.
- joblib for loading the persisted model pipeline.
- Black, Ruff, MyPy, and pytest for quality checks.

## Application Entry Point

- Module: `backend/app/main.py`.
- ASGI application: `app`.
- Factory: `create_app()`.
- API prefix: `/api/v1`.
- OpenAPI metadata:
  - Title: configured by `APP_NAME`.
  - Version: configured by `API_VERSION`.
  - Description: `API for customer support category inference.`

The application must enable CORS using `CORS_ALLOWED_ORIGINS` and must register
safe exception handlers before serving requests.

## Configuration

Configuration is loaded from environment variables and `.env` files through
`backend/app/core/config.py`.

Required and default settings:

| Variable | Default | Purpose |
| --- | --- | --- |
| `APP_ENV` | `local` | Runtime environment name. |
| `APP_NAME` | `Customer Support Classifier API` | FastAPI app title. |
| `API_VERSION` | `1.0.0` | API and health response version. |
| `BACKEND_HOST` | `0.0.0.0` | Server bind host. |
| `BACKEND_PORT` | `8000` | Server bind port. |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:4200` | Comma-separated allowed frontend origins. |
| `MODEL_ARTIFACT_PATH` | `ml/models/modelo_idf.joblib` | Full model pipeline artifact. |
| `MODEL_METADATA_PATH` | `ml/models/model_metadata.json` | Optional model metadata JSON. |
| `MODEL_VERSION` | `1.0.0` | Fallback model version. |
| `PIPELINE_VERSION` | `1.0.0` | Fallback pipeline version. |
| `LOG_LEVEL` | `INFO` | Logging level. |

Secrets must not be hardcoded in source, tests, Docker files, or examples.

## Endpoints

### `GET /api/v1/health`

Returns process health without exposing internals.

Response `200`:

```json
{
  "status": "ok",
  "service": "backend",
  "version": "1.0.0"
}
```

Contract:

- `status` must be `ok` while the application process is alive.
- `service` must be `backend`.
- `version` must equal the configured `API_VERSION`.
- The endpoint must be included in OpenAPI documentation.

### `POST /api/v1/predictions`

Predicts the customer support category for one request.

Request body:

```json
{
  "instruction": "Where is my order?"
}
```

Validation:

- `instruction` is required.
- Minimum length after trimming: 1 character.
- Maximum length: 5000 characters.
- Blank text must be rejected with HTTP `422`.

Response `200`:

```json
{
  "prediction": "ORDER",
  "confidence": 0.92,
  "model_version": "1.0.0",
  "pipeline_version": "1.0.0"
}
```

`confidence` may be `null` when the loaded pipeline does not expose
`predict_proba`.

Supported prediction categories:

- `ORDER`
- `SHIPPING`
- `CANCEL`
- `INVOICE`
- `PAYMENT`
- `REFUND`
- `FEEDBACK`
- `CONTACT`
- `ACCOUNT`
- `DELIVERY`
- `SUBSCRIPTION`

## Model Loading and Inference

The backend must load a complete scikit-learn compatible pipeline from
`MODEL_ARTIFACT_PATH`. The artifact must expose `predict`.

Inference behavior:

1. Validate `PredictionInput`.
2. Build a pandas `DataFrame` with one column: `instruction`.
3. Call `pipeline.predict(features)`.
4. Verify the returned category is one of the supported categories.
5. Call `pipeline.predict_proba(features)` when available and return the maximum
   probability as confidence.
6. Return model and pipeline versions from metadata when available, otherwise
   use configured defaults.

The backend must not expose raw model internals in API responses.

## Error Handling

When the model artifact is missing, invalid, or metadata cannot be read, the API
must return HTTP `503` with a safe Spanish message:

```json
{
  "detail": "El modelo de prediccion no esta disponible.",
  "error_code": "MODEL_NOT_LOADED"
}
```

Validation errors may use FastAPI's standard `422` response. User-facing error
messages must be Spanish and must not include stack traces or secret values.

## CORS and Frontend Integration

The backend must allow the Angular development origin by default:

```text
http://localhost:4200
```

Additional origins must be supplied through `CORS_ALLOWED_ORIGINS` as a
comma-separated environment variable.

## Testing Requirements

Backend tests must cover:

- `GET /api/v1/health` response shape.
- `POST /api/v1/predictions` success response.
- Request validation for blank `instruction`.
- Model loading behavior and unavailable-model errors.
- Service-layer handling of pipelines with and without `predict_proba`.

Required validation commands:

```powershell
cd backend
..\.venv\Scripts\python.exe -m black app
..\.venv\Scripts\python.exe -m ruff check app
..\.venv\Scripts\python.exe -m mypy app
..\.venv\Scripts\python.exe -m pytest
```

## Compliance and Security Notes

- Do not log full user requests when they may contain personal data.
- Do not log model artifacts, secrets, or environment values containing
  credentials.
- Keep prediction responses limited to category, optional confidence, and
  version metadata.
- Treat model performance, limitations, and training dataset provenance as
  documentation obligations, not legal certification.
