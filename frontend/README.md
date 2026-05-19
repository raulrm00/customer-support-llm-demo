# Frontend - Customer Support Classifier

Angular application for interacting with the Customer Support Classifier API.

## Features

- **Interactive UI**: Submit requests and see predictions in real-time.
- **Spanish Interface**: All user-facing text is in Spanish (Labels, messages, etc.).
- **Responsive Design**: Built with Tailwind CSS for a modern, accessible experience.
- **Type Safe**: Fully typed API contracts and components.

## Local Setup

1. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Run development server**:
   ```bash
   npm start
   ```
   Once running, navigate to `http://localhost:4200/`.

## Docker

### Build Image
Execute from the `frontend/` directory:
```bash
cd frontend
docker build -t customer-support-frontend .
```

### Run Container
```bash
docker run -p 4200:4200 customer-support-frontend
```

## Quality Assurance

```bash
cd frontend
npm test        # Run unit tests
npm run build   # Production build validation
```

## Implementation Details

- **Framework**: Angular (Standalone Components, Signals).
- **Styling**: Tailwind CSS.
- **Language**: UI in Spanish, Technical Code in English.
- **Accessibility**: Follows WCAG AA standards and passes AXE checks.
- **Backend URL**: Configured via Angular environment files.
