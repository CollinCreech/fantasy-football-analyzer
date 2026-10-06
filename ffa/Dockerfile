FROM node:22-bookworm-slim AS frontend

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

COPY public ./public
COPY src ./src
RUN npm run build

FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

COPY backend ./backend
COPY --from=frontend /app/build ./build

RUN useradd --create-home appuser
USER appuser

CMD ["sh", "-c", "exec python -m uvicorn main:app --app-dir backend --host 0.0.0.0 --port ${PORT:-10000}"]