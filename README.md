# Customer Support AI Project

An end-to-end AI-powered system for automatically classifying customer support requests into actionable categories.

## Architecture Overview

- **Backend**: Python FastAPI service serving a fine-tuned Qwen-0.6B model wrapper.
- **Frontend**: Angular application (v20+) with Tailwind CSS styling and Spanish UI.
- **ML/Data**: DVC-managed pipeline for Qwen SFT fine-tuning and model versioning.
- **Deployment**: Containerized using Docker and orchestrated with Docker Compose.

## Quick Start (Docker Compose)

The easiest way to run the entire system locally is using Docker Compose:

1. **Prepare environment**:
   ```bash
   cp .env.example .env
   ```

2. **Deploy the stack**:
   ```bash
   docker compose up --build
   ```

3. **Access the services**:
   - **Frontend**: [http://localhost:4200](http://localhost:4200)
   - **Backend API**: [http://localhost:8000](http://localhost:8000)
   - **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)

## Repository Structure

- `backend/`: FastAPI application, Pydantic schemas, and Docker configuration.
- `frontend/`: Angular source code, Tailwind configuration, and Nginx Docker setup.
- `ml/`: Machine learning source code (src/), notebooks, and DVC configuration.
- `refs/`: Reference specifications and data samples (read-only).
- `.agent/`: AI agent development journal, decisions, and handoff notes.
- `docs/`: (Optional) Extended documentation.

## Development

For detailed development instructions, please refer to the specific component READMEs:

- [Backend Development](./backend/README.md)
- [Frontend Development](./frontend/README.md)
- [ML Pipeline](./ml/README.md)

## Compliance & Standards

This project adheres to strict coding and ethical standards:
- **Language**: User-facing UI in Spanish; technical code and docs in English.
- **GDPR**: Data minimization and privacy-aware development.
- **EU AI Act**: Transparency, robustness, and performance documentation.
- **ENS**: Security best practices (Least privilege, secure config, etc.).

See `AGENTS.md` for the full set of rules and guidelines.
