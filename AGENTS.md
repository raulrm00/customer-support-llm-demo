# AGENTS.md

## 1. Purpose

This file defines the working rules for AI coding agents contributing to this repository.

The project is an AI-based web application with:

- A Python/FastAPI backend.
- An Angular frontend.
- A machine learning training pipeline using scikit-learn.
- Model production/inference capabilities.
- Dataset versioning with DVC.
- Experiment tracking with DVCLive.
- Deployment through Docker Compose in the final phase.
- Compliance-aware development considering GDPR, the EU AI Act, and ENS requirements.

All code-facing documentation, source comments, commit messages, and technical notes should be written in English unless otherwise specified.

User-facing visible content, including web UI labels, messages, validation errors, and help text, must be written in Spanish.

---

## 2. High-Level Repository Structure

The repository should be organized as follows:

```text
.
├── AGENTS.md
├── README.md
├── .gitignore
├── .env.example
├── docker-compose.yml
├── refs/
├── .agent/
│   ├── journal.md
│   ├── decisions.md
│   └── handoff.md
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── core/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── models/
│   │   └── tests/
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── pyproject.toml
│   └── README.md
├── frontend/
│   ├── package.json
│   ├── package-lock.json
│   ├── angular.json
│   ├── src/
│   └── README.md
├── ml/
│   ├── data/
│   │   ├── raw/
│   │   ├── processed/
│   │   └── splits/
│   ├── models/
│   ├── notebooks/
│   ├── src/
│   │   ├── schemas/
│   │   ├── preprocessing/
│   │   ├── training/
│   │   ├── evaluation/
│   │   └── inference/
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── dvc.yaml
│   ├── params.yaml
│   └── README.md
├── docs/
│   ├── api/
│   ├── architecture/
│   ├── compliance/
│   └── operations/
└── scripts/
```

### Important directory rules

- `backend/` contains the FastAPI application and backend business logic.
- `frontend/` contains the Angular application.
- `ml/` contains all training, validation, preprocessing, evaluation, model persistence, and inference-support code.
- `refs/` contains user-provided reference material.
- `.agent/` contains the AI agent implementation journal and handoff notes.
- `docs/` contains project documentation generated or maintained during development.

---

## 3. Immutable Reference Material

The `refs/` directory is read-only for agents.

Agents must:

- Read files in `refs/` when they are relevant to the current task.
- Treat `refs/` as authoritative project input when it specifies expected system behavior.
- Never modify, delete, rename, move, reformat, or regenerate files inside `refs/`.
- Never overwrite user-provided documentation.
- If something in `refs/` conflicts with existing code, document the conflict in `.agent/decisions.md` and ask for clarification when necessary.
- If implementation assumptions are made based on `refs/`, record them in `.agent/journal.md`.

---

## 4. Agent Working Journal

Agents must maintain a development journal under `.agent/`.

The purpose of the journal is to allow future agents or developers to resume work without rereading the entire codebase.

### Required files

#### `.agent/journal.md`

Append an entry after each meaningful implementation step.

Each entry should include:

```markdown
## YYYY-MM-DD HH:MM - Short task title

### Goal
Briefly describe the task.

### Files changed
- `path/to/file`
- `path/to/other-file`

### Summary
Explain what was implemented or changed.

### Validation
List the commands run and their results.

### Next steps
Mention pending work, risks, or follow-up tasks.
```

#### `.agent/decisions.md`

Use this file to record relevant technical decisions.

Each decision should include:

```markdown
## YYYY-MM-DD - Decision title

### Context
What problem or trade-off was considered?

### Decision
What was decided?

### Rationale
Why was this option chosen?

### Consequences
What constraints, risks, or future tasks follow from this decision?
```

#### `.agent/handoff.md`

Keep this file updated with the current project status.

It should contain:

- Current implementation phase.
- Main working areas.
- Known blockers.
- Commands needed to run the project.
- Commands needed to run tests.
- Static analysis commands.
- Important environment variables.
- Known risks.
- Suggested next task.

---

## 5. Git Workflow

The project uses Git for version control.

Agents must:

- Keep changes focused and atomic.
- Avoid mixing unrelated changes in the same commit.
- Check the working tree before and after modifications.
- Never overwrite user changes.
- Never force-push.
- Never delete branches unless explicitly instructed.
- Prefer clear commit messages.

Recommended commit message format:

```text
type(scope): short description
```

Examples:

```text
feat(api): add prediction endpoint
feat(api): add health endpoint
test(ml): add dataset schema validation tests
docs(compliance): add GDPR risk notes
chore(docker): add backend service to compose file
```

Common types:

- `feat`
- `fix`
- `test`
- `docs`
- `refactor`
- `chore`
- `ci`
- `build`

---

## 6. Environment Configuration

Environment variables must be loaded from a `.env` file during local development.

Rules:

- `.env` must never be committed.
- `.env.example` must be committed.
- Any new required environment variable must be added to `.env.example`.
- Sensitive values must never be hardcoded in source code, tests, documentation examples, or Docker files.
- Use explicit configuration classes in the backend, preferably based on Pydantic settings.

Example `.env.example` structure:

```env
APP_ENV=local
APP_NAME=ai-application
API_VERSION=1.0.0
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

CORS_ALLOWED_ORIGINS=http://localhost:4200

MODEL_ARTIFACT_PATH=ml/models/model_pipeline.joblib

LOG_LEVEL=INFO

# External APIs
EXTERNAL_API_BASE_URL=
EXTERNAL_API_KEY=
```

---

## 7. Python Backend Standards

The backend must be implemented using:

- Python.
- FastAPI.
- Pydantic for data validation.
- Type hints.
- Black for formatting.
- Ruff for linting and static analysis.
- MyPy for optional but recommended type checking.
- Unit tests for core functionality.

### Backend design principles

- Keep route handlers thin.
- Put business logic in service modules.
- Put request and response schemas in dedicated Pydantic schema modules.
- Validate all external inputs.
- Return predictable error responses.
- Avoid global mutable state.
- Use dependency injection where appropriate.
- Keep model inference logic isolated from API routing logic.
- Version API routes explicitly.
- Provide a mandatory health endpoint.

Recommended API route prefix:

```text
/api/v1
```

### Required health endpoint

The backend must expose a health endpoint that can be used by developers, deployment tooling, and Docker health checks.

Required path:

```text
GET /api/v1/health
```

Minimum response shape:

```json
{
  "status": "ok",
  "service": "backend",
  "version": "1.0.0"
}
```

The health endpoint should:

- Return HTTP `200` when the application process is alive.
- Include the API version.
- Avoid exposing secrets or internal infrastructure details.
- Optionally include dependency checks under a separate readiness endpoint if needed.

Recommended future endpoints:

```text
GET /api/v1/health
GET /api/v1/readiness
GET /api/v1/liveness
```

### Example backend layout

```text
backend/app/
├── main.py
├── api/
│   └── v1/
│       ├── router.py
│       ├── health.py
│       └── predictions.py
├── core/
│   ├── config.py
│   ├── logging.py
│   └── errors.py
├── schemas/
│   ├── prediction.py
│   └── health.py
├── services/
│   ├── prediction_service.py
│   └── model_loader.py
├── models/
└── tests/
```

### Python style

- Use type hints for all public functions.
- Use docstrings for public modules, classes, and functions.
- Use Black formatting.
- Use Ruff for linting and static analysis.
- Use MyPy when type checking is practical for the current codebase.
- Prefer small, composable functions.
- Avoid deeply nested control flow.
- Avoid broad `except Exception` unless properly logged and justified.
- Do not silently swallow errors.
- Use structured logging instead of `print`.

Example docstring style:

```python
def predict(input_data: PredictionInput) -> PredictionOutput:
    """Generate a prediction using the currently loaded model pipeline.

    Args:
        input_data: Validated prediction input payload.

    Returns:
        A validated prediction output object.

    Raises:
        ModelNotLoadedError: If the model pipeline cannot be loaded.
    """
```

### Formatting and static analysis

Run Black before finalizing Python changes:

```bash
cd backend
black app
```

Run Ruff after backend modifications:

```bash
cd backend
ruff check app
```

Run MyPy when type checking is configured:

```bash
cd backend
mypy app
```

For ML code:

```bash
cd ml
black src
ruff check src
mypy src
```

---

## 8. FastAPI and OpenAPI Requirements

The backend must expose OpenAPI documentation.

Rules:

- The OpenAPI schema must reflect the current API behavior.
- API routes must be versioned using semantic versioning.
- The API version must be configurable.
- Breaking changes must increment the major version.
- Backward-compatible additions should increment the minor version.
- Fixes that do not change the API contract should increment the patch version.
- Public request and response models must use Pydantic schemas.
- Endpoint descriptions should be clear and useful.
- The health endpoint must be included in the OpenAPI documentation.

Recommended metadata:

```python
app = FastAPI(
    title="AI Application API",
    version=settings.api_version,
    description="API for model training, inference, and application services.",
)
```

Generated OpenAPI documentation should be stored or referenced under:

```text
docs/api/
```

---

## 9. Machine Learning Standards

The ML subsystem must support:

- Dataset validation.
- Cleaning and preprocessing.
- Training.
- Evaluation.
- Experiment tracking.
- Full pipeline persistence.
- Production inference handoff.

Required libraries:

- scikit-learn.
- pandas.
- pandera.
- joblib.
- dvc.
- dvclive.

### ML directory responsibilities

```text
ml/src/schemas/
```

Contains Pandera dataset schemas.

```text
ml/src/preprocessing/
```

Contains cleaning, feature engineering, transformation, and preprocessing code.

```text
ml/src/training/
```

Contains training scripts and reusable training functions.

```text
ml/src/evaluation/
```

Contains metrics, validation, and evaluation utilities.

```text
ml/src/inference/
```

Contains inference helpers shared with production code where appropriate.

```text
ml/models/
```

Contains trained model artifacts and full model pipelines tracked according to project policy.

### Dataset validation with Pandera

All training scripts must validate input datasets before training.

Rules:

- Define explicit Pandera schemas for raw, processed, and split datasets where applicable.
- Fail early if required columns are missing.
- Validate data types.
- Validate nullability.
- Validate value ranges when relevant.
- Record validation failures clearly.

### Model and preprocessing pipeline persistence

Model persistence must include the complete cleaning and preprocessing pipeline as well as the trained model.

Agents must not persist only the estimator when production inference depends on preprocessing steps.

Required approach:

- Use scikit-learn `Pipeline` or compatible composed objects for preprocessing plus model inference.
- Include cleaning, transformation, feature engineering, encoding, scaling, imputation, and estimator steps where applicable.
- Persist the complete pipeline artifact using `joblib`.
- Ensure the same transformations used during training are used during inference.
- Add tests that load the persisted pipeline and perform inference on representative input.
- Document the expected input schema for the persisted pipeline.

Recommended pattern:

```python
from sklearn.pipeline import Pipeline
import joblib

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", estimator),
    ]
)

pipeline.fit(X_train, y_train)
joblib.dump(pipeline, model_artifact_path)
loaded_pipeline = joblib.load(model_artifact_path)
predictions = loaded_pipeline.predict(X_new)
```

The persisted artifact should include enough metadata to identify:

- Training dataset version.
- Training parameters.
- Preprocessing steps.
- Feature schema.
- Metric results.
- Code version or Git commit when available.
- Creation timestamp.
- Intended inference schema.
- Model or pipeline semantic version.

Recommended artifact naming:

```text
ml/models/model_pipeline.joblib
ml/models/model_metadata.json
```

---

## 10. DVC and Dataset Versioning

The project uses DVC to version datasets and ML pipeline artifacts.

Agents must:

- Use DVC for raw, processed, and split datasets.
- Avoid committing large datasets directly to Git.
- Track dataset changes through DVC.
- Keep `dvc.yaml` and `params.yaml` updated.
- Document data pipeline stages.
- Never modify or delete data without a clear task requirement.
- Never expose sensitive or personal data in logs, docs, or examples.

Recommended dataset layout:

```text
ml/data/raw/
ml/data/processed/
ml/data/splits/
```

Recommended DVC commands:

```bash
cd ml
dvc status
dvc repro
dvc metrics show
```

If a dataset or artifact is too large or sensitive, document the expected DVC workflow without embedding the data in the repository.

---

## 11. DVCLive Experiment Tracking

Training scripts should use DVCLive to log:

- Parameters.
- Metrics.
- Plots when useful.
- Model and pipeline metadata where appropriate.

Examples of metrics:

- Accuracy.
- Precision.
- Recall.
- F1 score.
- ROC AUC.
- MAE, RMSE, or R2 for regression tasks.
- Dataset size.
- Training duration.

Rules:

- Keep experiment outputs reproducible.
- Ensure parameters are read from `params.yaml` where practical.
- Log enough context to compare experiments meaningfully.
- Do not log personal data or sensitive raw samples.
- Record preprocessing and feature engineering configuration as part of the experiment context.

---

## 12. Frontend Standards

The frontend must be implemented using Angular.

Rules:

- User-visible text must be in Spanish.
- Keep components focused and small.
- Use Angular services for API communication.
- Use typed interfaces for API contracts.
- Keep environment-specific configuration in Angular environment files.
- Do not hardcode backend URLs in components.
- Validate user inputs before submitting requests.
- Display clear Spanish error messages.
- Avoid leaking technical exception details to end users.
- Add tests for core components and services.

Recommended frontend layout:

```text
frontend/src/app/
├── core/
├── shared/
├── features/
│   ├── predictions/
│   └── dashboard/
├── services/
├── models/
└── app.routes.ts
```

### UI language rule

All visible UI text must be Spanish.

Examples:

```text
Correct:
- "Enviar"
- "Se ha producido un error"
- "Resultado de la predicción"

Incorrect:
- "Submit"
- "An error occurred"
- "Prediction result"
```

Technical code names, interfaces, classes, and comments should remain in English.

---

## 13. Dependency Management

### Python

Use dependency control files.

For backend:

```text
backend/requirements.txt
backend/requirements-dev.txt
```

For ML:

```text
ml/requirements.txt
ml/requirements-dev.txt
```

Agents must:

- Add runtime dependencies to `requirements.txt`.
- Add test, linting, static analysis, formatting, and development dependencies to `requirements-dev.txt`.
- Include `black`, `ruff`, `pytest`, and, when configured, `mypy` in the relevant development requirements.
- Avoid adding unnecessary dependencies.
- Prefer stable, widely used packages.
- Keep dependency changes explicit.

### Node / Angular

Use:

```text
frontend/package.json
frontend/package-lock.json
```

Rules:

- Add dependencies with npm.
- Do not manually edit lockfiles unless necessary.
- Keep production and development dependencies separate.
- Avoid unnecessary frontend packages.

---

## 14. Python Virtual Environments

During initial development, use Python virtual environments.

Recommended setup:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
pip install -r backend/requirements-dev.txt
pip install -r ml/requirements.txt
pip install -r ml/requirements-dev.txt
```

If working from Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
pip install -r backend/requirements-dev.txt
pip install -r ml/requirements.txt
pip install -r ml/requirements-dev.txt
```

The `.venv/` directory must not be committed.

---

## 15. Testing Requirements

Unit tests are required for core functionality.

Agents must:

- Add or update tests when changing behavior.
- Run relevant tests after every code modification.
- Run static analysis after backend and ML code modifications.
- Run the full test suite before considering the task complete when practical.
- Document test and static analysis commands and their results in `.agent/journal.md`.
- Never ignore failing tests.
- If a test or static analysis command cannot be run, document the reason clearly.

### Backend tests

Recommended command:

```bash
cd backend
pytest
```

Backend test coverage should include:

- Health endpoint behavior.
- Pydantic schema validation.
- Service-layer logic.
- Prediction endpoint behavior.
- Error handling.
- Model pipeline loading behavior.

### Backend static analysis

Recommended commands:

```bash
cd backend
ruff check app
mypy app
```

At minimum, Ruff must be used after backend code changes. MyPy should be used when configured and practical.

### ML tests

Recommended command:

```bash
cd ml
pytest
```

ML test coverage should include:

- Pandera schema validation.
- Feature preprocessing.
- Cleaning pipeline behavior.
- Training function behavior.
- Evaluation metric calculation.
- Full pipeline persistence and loading.
- Inference input/output compatibility.

### Frontend tests

Recommended command:

```bash
cd frontend
npm test
```

Frontend test coverage should include:

- Core components.
- API services.
- Form validation.
- Error state rendering.
- Main user flows.

---

## 16. Validation After Changes

After modifying code, agents must run the relevant validation commands.

Minimum expected validation:

### Python backend changes

```bash
cd backend
black app
ruff check app
pytest
```

When MyPy is configured:

```bash
cd backend
mypy app
```

### ML changes

```bash
cd ml
black src
ruff check src
pytest
```

When MyPy is configured:

```bash
cd ml
mypy src
```

If DVC pipeline stages are affected:

```bash
cd ml
dvc repro
dvc metrics show
```

### Angular changes

```bash
cd frontend
npm test
npm run build
```

### Docker changes

```bash
docker compose config
docker compose build
```

If a command fails:

- Do not hide the failure.
- Investigate and fix the cause when possible.
- Record the failure and status in `.agent/journal.md`.
- Do not claim completion unless the validation status is clear.

---

## 17. Docker Compose Deployment

In the final project phase, the system must be containerized using Docker Compose.

Expected services may include:

- `backend`
- `frontend`
- Optional model-serving or worker service
- Optional database
- Optional reverse proxy

Rules:

- Use `.env` for runtime configuration.
- Do not bake secrets into images.
- Keep Dockerfiles minimal and explicit.
- Prefer reproducible builds.
- Expose only required ports.
- Include health checks where practical.
- Backend Docker health checks should use `GET /api/v1/health` unless a dedicated readiness endpoint is introduced.
- Document deployment commands in `docs/operations/`.

Recommended commands:

```bash
docker compose build
docker compose up
docker compose down
```

---

## 18. Security, Privacy, and Compliance-Aware Development

The project must be developed with GDPR, the EU AI Act, and ENS requirements in mind where applicable.

Agents are not expected to provide legal certification, but must implement and document reasonable technical and organizational measures.

### GDPR considerations

Agents should consider:

- Data minimization.
- Purpose limitation.
- Lawful basis assumptions.
- Personal data identification.
- Avoiding unnecessary personal data storage.
- Secure handling of personal data.
- Access control.
- Retention policies.
- Auditability.
- User rights support where applicable.
- Avoiding sensitive data exposure in logs.
- Avoiding personal data in test fixtures unless anonymized or synthetic.

### EU AI Act considerations

Agents should consider:

- Intended purpose of the AI system.
- Risk classification assumptions.
- Dataset quality and representativeness.
- Human oversight needs.
- Transparency requirements.
- Logging and traceability.
- Model performance documentation.
- Bias and robustness evaluation where applicable.
- Clear limitations of the model.
- Post-deployment monitoring needs.

### ENS considerations

Agents should consider:

- Authentication and authorization.
- Secure configuration.
- Traceability and logging.
- Backup and recovery expectations.
- Dependency and vulnerability management.
- Secure communications.
- Principle of least privilege.
- Environment separation.
- Incident response documentation.
- System hardening where applicable.

### Compliance documentation

In the final phase, generate documentation under:

```text
docs/compliance/
```

Recommended files:

```text
docs/compliance/gdpr-assessment.md
docs/compliance/ai-act-assessment.md
docs/compliance/ens-assessment.md
docs/compliance/risk-register.md
docs/compliance/data-inventory.md
docs/compliance/model-card.md
```

Each compliance document should clearly distinguish:

- Implemented controls.
- Partially implemented controls.
- Open risks.
- Assumptions.
- Required human/legal review.

---

## 19. API and Model Contract Compatibility

The backend API and ML inference code must remain compatible.

Rules:

- Define explicit input and output schemas.
- Validate inference input before passing it to the model pipeline.
- Validate or normalize model output before returning it to API clients.
- Avoid exposing raw model internals through API responses.
- Keep model and pipeline version metadata available.
- Add tests for API-to-model integration.
- Document breaking changes.

Recommended prediction response fields:

```json
{
  "prediction": "...",
  "confidence": 0.95,
  "model_version": "1.0.0",
  "pipeline_version": "1.0.0"
}
```

Adjust the exact schema to the project requirements.

---

## 20. Documentation Standards

Agents must keep documentation current.

Documentation should include:

- Setup instructions.
- Development workflow.
- Test commands.
- Static analysis commands.
- API documentation.
- ML pipeline usage.
- Model pipeline persistence and loading.
- DVC usage.
- Docker Compose deployment.
- Environment variables.
- Compliance notes.
- Architecture decisions.

Technical documentation should be in English unless the project owner requests otherwise.

User-facing documentation may be in Spanish when intended for end users.

---

## 21. Error Handling and Logging

Backend rules:

- Use structured logging.
- Do not log secrets.
- Do not log full personal records.
- Map internal errors to safe API responses.
- Keep error messages useful but not overly revealing.
- Include request correlation IDs if introduced.
- Centralize common exception handling.
- Keep health endpoint responses safe and minimal.

Frontend rules:

- Show user-friendly Spanish error messages.
- Do not expose stack traces.
- Handle network failures gracefully.
- Handle validation errors clearly.

ML rules:

- Fail fast on invalid datasets.
- Log training progress without leaking sensitive data.
- Store metrics and parameters, not raw sensitive samples.
- Log pipeline configuration without exposing sensitive data.

---

## 22. Code Quality Principles

Agents must follow these principles:

- Prefer clarity over cleverness.
- Keep modules cohesive.
- Keep functions small.
- Avoid duplication.
- Use explicit names.
- Avoid premature optimization.
- Add tests before or alongside behavior changes.
- Refactor only when it supports the current task.
- Maintain separation of concerns.
- Keep frontend, backend, and ML responsibilities distinct.
- Avoid adding hidden behavior.
- Avoid unnecessary global state.
- Keep configuration externalized.

---

## 23. Accessibility and UX

For the Angular frontend:

- Use semantic HTML where possible.
- Ensure forms have labels.
- Ensure errors are readable and associated with inputs.
- Avoid color-only indicators.
- Use Spanish UI text.
- Keep loading states clear.
- Keep empty states clear.
- Keep user actions reversible where practical.

---

## 24. External APIs and Integrations

When integrating external APIs:

- Store credentials in environment variables.
- Document required variables in `.env.example`.
- Add timeouts.
- Handle failures explicitly.
- Avoid logging tokens or secrets.
- Wrap external calls in services.
- Add tests using mocks.
- Document assumptions in `.agent/decisions.md` when the integration behavior is unclear.

If external API documentation is placed in `refs/`, treat it as read-only.

---

## 25. Prohibited Agent Actions

Agents must not:

- Modify files inside `refs/`.
- Commit `.env`.
- Commit secrets, credentials, private keys, tokens, or passwords.
- Commit virtual environments.
- Commit large datasets directly to Git when they should be tracked with DVC.
- Skip tests after code changes.
- Skip static analysis after backend code changes.
- Claim tests or static analysis passed without running them.
- Remove tests to make the suite pass unless explicitly justified.
- Hide failing validations.
- Persist only the estimator when inference depends on preprocessing.
- Introduce user-facing English text in the Angular UI.
- Hardcode production configuration.
- Delete user work.
- Make legal compliance claims without qualification.
- Treat compliance documentation as legal advice or certification.

---

## 26. Initial Project Setup Checklist

When initializing the repository, agents should create or verify:

- Git repository initialized.
- `.gitignore`.
- `.env.example`.
- `.agent/journal.md`.
- `.agent/decisions.md`.
- `.agent/handoff.md`.
- `backend/` structure.
- `frontend/` Angular project structure.
- `ml/` structure.
- Python virtual environment instructions.
- Backend `requirements.txt`.
- Backend `requirements-dev.txt` including `black`, `ruff`, `pytest`, and optionally `mypy`.
- ML `requirements.txt`.
- ML `requirements-dev.txt` including `black`, `ruff`, `pytest`, and optionally `mypy`.
- Frontend `package.json`.
- Basic FastAPI app.
- Mandatory backend health endpoint at `GET /api/v1/health`.
- Basic Angular app.
- Initial backend tests.
- Initial frontend tests.
- Initial ML validation tests.
- Initial full-pipeline persistence test for ML.
- DVC initialization.
- Initial documentation under `docs/`.

---

## 27. Task Completion Checklist

Before marking a task complete, agents must verify:

- Code is implemented in the correct module.
- User-facing frontend text is in Spanish.
- Python code is formatted with Black.
- Ruff static analysis was run for modified backend or ML code.
- MyPy was run if configured.
- Relevant unit tests were added or updated.
- Relevant tests were run.
- DVC pipeline was checked if data or ML pipeline changed.
- Persisted ML artifacts include the complete preprocessing and model pipeline when applicable.
- `.env.example` was updated if configuration changed.
- Documentation was updated if behavior changed.
- `.agent/journal.md` was updated.
- `.agent/handoff.md` was updated if project state changed.
- No files in `refs/` were modified.
- No secrets were added.
- Known limitations were documented.

---

## 28. Recommended Commands Reference

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
black app
ruff check app
mypy app
pytest
uvicorn app.main:app --reload
```

Health endpoint check:

```bash
curl http://localhost:8000/api/v1/health
```

### ML

```bash
cd ml
pip install -r requirements.txt -r requirements-dev.txt
black src
ruff check src
mypy src
pytest
dvc status
dvc repro
dvc metrics show
```

### Frontend

```bash
cd frontend
npm install
npm test
npm run build
npm start
```

### Docker Compose

```bash
docker compose config
docker compose build
docker compose up
docker compose down
```

---

## 29. Final Phase Deliverables

Before the final delivery phase, the repository should contain:

- Working FastAPI backend.
- Mandatory backend health endpoint.
- Working Angular frontend.
- Tested ML training pipeline.
- Persisted full preprocessing-plus-model pipeline using joblib.
- Dataset versioning with DVC.
- Experiment tracking with DVCLive.
- Docker Compose deployment.
- OpenAPI documentation.
- Developer setup documentation.
- Static analysis documentation and commands.
- Operations documentation.
- Compliance assessment documentation for GDPR, EU AI Act, and ENS.
- Updated `.agent/` journal and handoff files.

---

## 30. Operating Principle

When uncertain, agents should:

1. Inspect existing code and documentation.
2. Read relevant files in `refs/` without modifying them.
3. Prefer small, reversible changes.
4. Add tests for changed behavior.
5. Run formatting, static analysis, and validation commands.
6. Record the work in `.agent/journal.md`.
7. Clearly document assumptions, risks, and next steps.
