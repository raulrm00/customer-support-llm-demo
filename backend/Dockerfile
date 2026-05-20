# Stage 1: Build dependencies
FROM python:3.13-alpine AS builder

# Install build dependencies for pandas, numpy, and scikit-learn
RUN apk add --no-cache \
    g++ \
    musl-dev \
    python3-dev \
    openblas-dev \
    libstdc++

WORKDIR /build

# Install dependencies into a wheels directory
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip wheel --no-cache-dir --wheel-dir /build/wheels -r requirements.txt

# Stage 2: Final image
FROM python:3.13-alpine

# Install runtime dependencies
RUN apk add --no-cache \
    libstdc++ \
    openblas \
    libgomp \
    curl

WORKDIR /app

# Copy wheels from builder and install them
COPY --from=builder /build/wheels /wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels /wheels/* && \
    rm -rf /wheels

# Copy backend application
COPY backend/app /app/backend/app

# Copy model artifacts (excluding training logic)
# Note: These files are expected to be available in the build context
COPY ml/models/modelo_idf.joblib /app/ml/models/modelo_idf.joblib
COPY ml/models/model_metadata.json /app/ml/models/model_metadata.json

# Environment configuration
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    APP_ENV=production \
    BACKEND_HOST=0.0.0.0 \
    BACKEND_PORT=8000 \
    MODEL_ARTIFACT_PATH=/app/ml/models/modelo_idf.joblib \
    MODEL_METADATA_PATH=/app/ml/models/model_metadata.json \
    PYTHONPATH=/app/backend

# Expose the API port
EXPOSE 8000

# Launch the API with uvicorn
# We set the working directory to where the app package is located
WORKDIR /app/backend
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
