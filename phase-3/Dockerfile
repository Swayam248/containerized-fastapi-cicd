# =========================
# Stage 1: Builder
# =========================
FROM python:3.12-alpine AS builder

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# =========================
# Stage 2: Final Image
# =========================
FROM python:3.12-alpine

WORKDIR /app

# Copy only installed Python packages
COPY --from=builder /install /usr/local

# Create non-root user
RUN addgroup -S appgroup && \
    adduser -S appuser -G appgroup

COPY app/ ./app/

# Run application as non-root user
USER appuser

EXPOSE 8000

# Container health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]