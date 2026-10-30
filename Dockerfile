# Stage 1: Build & Runtime
FROM python:3.12-slim

# Prevent Python from writing .pyc files and buffer outputs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production
ENV PORT=5000

# Set working directory
WORKDIR /app

# Install essential build packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Run as non-privileged system user for container security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose default HTTP port
EXPOSE 5000

# Docker healthcheck pinging /health route
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Launch production WSGI application server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--threads", "2", "--timeout", "60", "run:app"]
