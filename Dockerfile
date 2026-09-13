FROM node:20-slim AS frontend-build

WORKDIR /frontend

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build


FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://deno.land/install.sh | sh

WORKDIR /app

ENV PYTHONPATH="/app/docker/app"
ENV PATH="/root/.deno/bin:${PATH}"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY --from=frontend-build /frontend/dist ./frontend/dist

RUN mkdir -p /audio /var/log/metrics

EXPOSE 3000

CMD ["gunicorn", "-w", "4", "--timeout", "240", "--bind", "0.0.0.0:3000", "app:app"]
