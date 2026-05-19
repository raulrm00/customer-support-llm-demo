# Stage 1: Build the Angular application
FROM node:22-alpine AS builder

WORKDIR /app

# Copy package management files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application source code
COPY . .

# Environment variable for the backend API URL used during build
# Defaults to the backend service on port 8000
ARG API_BASE_URL=http://localhost:8000/api/v1
RUN sed -i "s|apiBaseUrl: '.*'|apiBaseUrl: '$API_BASE_URL'|g" src/environments/environment.ts && \
    sed -i "s|apiBaseUrl: '.*'|apiBaseUrl: '$API_BASE_URL'|g" src/environments/environment.development.ts && \
    sed -i "s|production: false|production: true|g" src/environments/environment.ts && \
    sed -i "s|production: false|production: true|g" src/environments/environment.development.ts

# Build the application for production
RUN npm run build -- --configuration production

# Stage 2: Serve the application using Nginx
FROM nginx:alpine

# Copy built artifacts from the builder stage to Nginx html directory
# Default output directory for @angular/build:application is dist/frontend/browser
COPY --from=builder /app/dist/frontend/browser /usr/share/nginx/html

# Copy custom nginx configuration for SPA routing if needed
# For simplicity, we'll use a basic redirect to index.html for all paths
RUN echo 'server { \
    listen 4200; \
    location / { \
        root /usr/share/nginx/html; \
        index index.html index.htm; \
        try_files $uri $uri/ /index.html; \
    } \
}' > /etc/nginx/conf.d/default.conf

# Expose the requested port
EXPOSE 4200

# Set environment variables for production deployment reference
ENV APP_ENV=production \
    BACKEND_PORT=8000 \
    API_BASE_URL=http://localhost:8000/api/v1

CMD ["nginx", "-g", "daemon off;"]
