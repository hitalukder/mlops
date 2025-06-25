# Use a slim Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy source code into container
COPY . .

# Install OS dependencies (optional: for time zone, debugging, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install required Python packages
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    requests \
    prometheus-client \
    "opentelemetry-api>=1.26.0,<1.27.0" \
    "opentelemetry-sdk>=1.26.0,<1.27.0" \
    "opentelemetry-exporter-otlp-proto-grpc>=1.26.0,<1.27.0" \
    "opentelemetry-instrumentation-fastapi" \
    "opentelemetry-instrumentation-requests" \
    "opentelemetry-exporter-prometheus"

# Expose FastAPI HTTP and Prometheus metrics port
EXPOSE 8002
EXPOSE 8001

# Run FastAPI app via uvicorn
CMD ["uvicorn", "rag_app:app", "--host", "0.0.0.0", "--port", "8002"]
