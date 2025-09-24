# Multi-stage Docker build for Tokyo Trip Assistant
FROM python:3.13-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install UV package manager
RUN pip install uv

# Copy dependency files first for better caching
COPY pyproject.toml ./
COPY uv.lock ./

# Install Python dependencies using uv sync (production only, no dev deps)
RUN uv sync --frozen --no-dev

# Copy application code
COPY app/ ./app/
COPY ui.py ./
COPY start.sh ./

# Make start script executable
RUN chmod +x start.sh

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose both ports
EXPOSE 8000 8501

# Health check (check both services)
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health && curl -f http://localhost:8501/_stcore/health || exit 1

# Start both services
CMD ["./start.sh"]