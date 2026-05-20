# Frontend - Customer Support Classifier

Angular frontend for interacting with the Customer Support Classifier API. The UI is Spanish-first for end users; technical code and docs are English.

## Features
- Interactive UI to submit requests and display predictions.
- Spanish user-facing text and accessible components.
- Tailwind CSS for responsive styling.
- Typed HTTP contracts and services.

## Local development
1. Install dependencies:

```bash
cd frontend
npm install
```

2. Start development server:

```bash
npm start
```

Visit: http://localhost:4200/

## Build & Docker
Build locally:

```bash
cd frontend
npm run build
```

Build Docker image (from `frontend/`):

```bash
docker build -t customer-support-frontend .
```

Run container:

```bash
docker run -p 4200:4200 customer-support-frontend
```

## Testing & QA
- Unit tests: `npm test`
- CI: Run `npm ci` and `npm run build` to validate changes.
- Accessibility: Use axe or cypress-axe in CI for important flows.

## Configuration
- Backend URL and environment-specific values are configured in `src/environments/*.ts`.
- Do not hardcode backend URLs in components; use environment files.

## Recommendations
- Keep user-facing strings in Spanish.
- Add E2E tests for main user flows (submit prediction, show result, error states).
- Run `npm run lint` as part of pre-commit or CI.
