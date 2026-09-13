# ---- Stage 1: build the React/Vite frontend ----
FROM node:20-slim AS frontend-build

WORKDIR /frontend

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build


# ---- Stage 2: Python backend ----
FROM python:3.13-slim AS backend

# ffmpeg is required by the backend
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the main/root Flask application
COPY app.py .

# The actual backend handler modules live here.
# Copy them into /app because app.py imports them as top-level modules.
COPY docker/app/*.py .

# Build frontend
COPY --from=frontend-build /frontend/dist ./frontend/dist

# Runtime directories used by the application
RUN mkdir -p /audio /var/log/metrics

EXPOSE 3000

CMD ["gunicorn", "--bind", "0.0.0.0:3000", "app:app"]
