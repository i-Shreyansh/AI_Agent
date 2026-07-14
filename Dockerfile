# ---------- Stage 1: Builder ----------
FROM python:3.11 AS builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN python -m  pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .


# ---------- Stage 2: Final ----------
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy app code
COPY --from=builder /app /app

EXPOSE 8000

CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]