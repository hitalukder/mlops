FROM pytorch/pytorch:2.2.2-cuda11.8-cudnn8-runtime

RUN apt update && apt install -y git && apt clean

# Install vLLM + OpenTelemetry packages

RUN pip install --no-cache-dir vllm \
    "opentelemetry-sdk>=1.26.0,<1.27.0" \
    "opentelemetry-api>=1.26.0,<1.27.0" \
    "opentelemetry-exporter-otlp>=1.26.0,<1.27.0" \
    "opentelemetry-semantic-conventions-ai>=0.4.1,<0.5.0"

CMD ["echo", "'vllm_server'"]
