# Frontend Specification

## Purpose

The frontend is an Angular application that lets users submit a customer support
request and receive a categorical prediction from the FastAPI backend.

All visible UI text must be Spanish. Technical names, class names, interfaces,
file names, comments, and developer documentation remain in English.

## Runtime Stack

- Angular with TypeScript.
- Tailwind CSS for styling.
- Angular `HttpClient` for backend communication.
- Angular Reactive Forms for input validation.
- Jasmine/Karma or the repository-selected Angular test runner for unit tests.

## Required Project Layout

```text
frontend/
├── package.json
├── package-lock.json
├── angular.json
├── tailwind.config.js
├── postcss.config.js
├── src/
│   ├── styles.css
│   ├── environments/
│   │   ├── environment.ts
│   │   └── environment.development.ts
│   └── app/
│       ├── app.config.ts
│       ├── app.routes.ts
│       ├── core/
│       ├── models/
│       │   └── prediction.model.ts
│       ├── services/
│       │   └── prediction-api.service.ts
│       └── features/
│           └── predictions/
│               ├── prediction-page.component.ts
│               ├── prediction-page.component.html
│               └── prediction-page.component.spec.ts
```

## Tailwind Requirements

Tailwind must be the primary styling mechanism.

Required setup:

- Install `tailwindcss`, `postcss`, and `autoprefixer` as development
  dependencies.
- Configure `tailwind.config.js` content scanning for Angular templates and
  TypeScript files under `src/`.
- Add Tailwind directives to `src/styles.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

Component styles should use Tailwind utility classes in templates. Custom CSS
should be limited to global base styles or repeated patterns that Tailwind
cannot express cleanly.

## Environment Configuration

The backend URL must not be hardcoded in components.

Recommended environment shape:

```ts
export const environment = {
  production: false,
  apiBaseUrl: 'http://localhost:8000/api/v1',
};
```

Production builds must provide the deployment API URL through the Angular
environment system or deployment-time configuration.

## API Models

Create typed API contracts in `frontend/src/app/models/prediction.model.ts`.

```ts
export type SupportCategory =
  | 'ORDER'
  | 'SHIPPING'
  | 'CANCEL'
  | 'INVOICE'
  | 'PAYMENT'
  | 'REFUND'
  | 'FEEDBACK'
  | 'CONTACT'
  | 'ACCOUNT'
  | 'DELIVERY'
  | 'SUBSCRIPTION';

export interface PredictionRequest {
  instruction: string;
}

export interface PredictionResponse {
  prediction: SupportCategory;
  confidence: number | null;
  model_version: string;
  pipeline_version: string;
}
```

## API Service

Create `PredictionApiService` under `frontend/src/app/services/`.

Responsibilities:

- Inject Angular `HttpClient`.
- Read `apiBaseUrl` from the environment.
- Send `POST /predictions` requests.
- Return typed `Observable<PredictionResponse>`.
- Apply an HTTP timeout when practical.
- Map technical failures to UI-safe Spanish messages outside the raw service or
  through a small error adapter.

Expected method:

```ts
predict(request: PredictionRequest): Observable<PredictionResponse>
```

Request target:

```text
POST {apiBaseUrl}/predictions
```

## Prediction Feature

The first screen should be the usable prediction experience, not a marketing
landing page.

Required UI:

- A page title in Spanish, for example `Clasificador de solicitudes`.
- A labeled textarea for the support request.
- A submit button, for example `Predecir categoria`.
- Client-side validation for required text and maximum length.
- Loading state while the request is in progress.
- Success state showing:
  - Predicted category.
  - Confidence as a percentage when available.
  - Model version.
  - Pipeline version.
- Empty state before the first prediction.
- Error state with a safe Spanish message.

Visible UI text examples:

- `Solicitud del cliente`
- `Describe la solicitud que quieres clasificar.`
- `Predecir categoria`
- `Resultado de la prediccion`
- `Confianza`
- `El texto es obligatorio.`
- `No se pudo obtener la prediccion. Intentalo de nuevo.`

## UX and Accessibility

- Use semantic HTML.
- Associate labels with form controls.
- Do not rely on color alone to communicate errors or results.
- Keep buttons and form controls keyboard accessible.
- Disable submit while the form is invalid or a request is loading.
- Do not expose stack traces or backend internals to users.
- Keep layout responsive for mobile and desktop.

Recommended layout:

- Full-width application shell with a constrained content width.
- A compact form panel and a result panel.
- Tailwind classes for spacing, focus rings, borders, and state colors.
- Avoid decorative-heavy landing sections; this is an operational tool.

## Backend Contract

The frontend must integrate with the current backend contract.

Prediction request:

```json
{
  "instruction": "Where is my order?"
}
```

Prediction response:

```json
{
  "prediction": "ORDER",
  "confidence": 0.92,
  "model_version": "1.0.0",
  "pipeline_version": "1.0.0"
}
```

Backend development URL:

```text
http://localhost:8000/api/v1
```

Angular development origin:

```text
http://localhost:4200
```

The backend must include this origin in `CORS_ALLOWED_ORIGINS`.

## Testing Requirements

Frontend tests must cover:

- Rendering of the prediction form.
- Required and blank input validation.
- Disabled submit state while invalid or loading.
- Successful API response rendering.
- Error response rendering with Spanish copy.
- `PredictionApiService` request URL and payload.

Required validation commands:

```powershell
cd frontend
npm test
npm run build
```

## Implementation Notes

- Use Angular services for API communication; components must not build raw
  backend URLs.
- Keep API interfaces synchronized with the backend Pydantic schemas.
- Do not store submitted support text unless a future requirement explicitly
  defines retention, lawful basis, and privacy controls.
- Do not add analytics or external integrations without documenting required
  environment variables and privacy implications.
