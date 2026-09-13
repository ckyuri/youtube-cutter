# ---- Stage 1: build the React/Vite frontend ----
FROM node:20-slim AS frontend-build

WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build
# Assumes Vite's default output directory: frontend/dist

# ---- Stage 2: Python backend ----
FROM python:3.13-slim AS backend

# ffmpeg is required by the app; the repo's bundled macOS binary won't run on Linux,
# so install a Linux-native ffmpeg via apt instead.
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# app.py sets template_folder='frontend/dist', static_folder='frontend/dist/assets'
# so the built frontend needs to live at that exact path relative to app.py.
COPY --from=frontend-build /frontend/dist ./frontend/dist

EXPOSE 3000

CMD ["gunicorn", "--bind", "0.0.0.0:3000", "app:app"]
