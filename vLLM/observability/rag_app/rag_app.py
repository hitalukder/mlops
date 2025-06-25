# SPDX-License-Identifier: Apache-2.0
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
import random
import time
import requests

# --- OpenTelemetry Tracing + Metrics ---
from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

# --- Prometheus metrics server ---
from prometheus_client import start_http_server

# --- OpenTelemetry Configuration ---
SERVICE = "rag-fastapi-service"

# Tracing setup
resource = Resource(attributes={SERVICE_NAME: SERVICE})
trace_provider = TracerProvider(resource=resource)
trace.set_tracer_provider(trace_provider)

# Add OTLP exporter to Jaeger via gRPC (default OTLP/gRPC port: 4317)
otlp_exporter = OTLPSpanExporter(
    endpoint="grpc://jaeger:4317",  # internal Docker hostname or "localhost" outside
    insecure=True
)

trace_provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
trace_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

tracer = trace.get_tracer(__name__)

# Metrics setup
prometheus_reader = PrometheusMetricReader()
metrics.set_meter_provider(MeterProvider(metric_readers=[prometheus_reader]))
meter = metrics.get_meter(__name__)
request_counter = meter.create_counter(
    name="rag_requests_total",
    unit="1",
    description="Total RAG requests"
)

# Start Prometheus metrics endpoint
start_http_server(port=8001)

# --- FastAPI App Setup ---
app = FastAPI(title="RAG Pipeline Service")
FastAPIInstrumentor.instrument_app(app)
RequestsInstrumentor().instrument()

# --- Mock Vector DB ---
mock_vector_db = {
    "san francisco": ["San Francisco is a city in California.", "It is known for the Golden Gate Bridge."],
    "new york": ["New York is the most populous city in the USA.", "It is known as the Big Apple."]
}

# --- Input Model ---
class RAGRequest(BaseModel):
    query: str

# --- Simulate Embedding ---
def embed_query(query: str) -> List[float]:
    time.sleep(0.1)
    return [random.random() for _ in range(5)]

# --- Simulate Vector Search ---
def search_vector_db(query_vec: List[float]) -> List[str]:
    time.sleep(0.2)
    return mock_vector_db["san francisco"] if query_vec[0] < 0.5 else mock_vector_db["new york"]

# --- Simulate LLM ---
def generate_answer(context: List[str], query: str) -> str:
    prompt = f"{' '.join(context)}\nQ: {query}\nA:"

    headers = {"Content-Type": "application/json"}
    TraceContextTextMapPropagator().inject(headers)

    payload = {
        "model": "facebook/opt-125m",
        "prompt": prompt,
        "max_tokens": 50,
        "temperature": 0.7,
        "n": 1,
        "stop": ["\n"]
    }

    try:
        response = requests.post("http://vllm-server:8000/v1/completions", headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["text"].strip()
    except Exception as e:
        return f"[Error generating response: {e}]"

# --- Endpoint ---
@app.post("/rag")
async def rag_pipeline(request: Request, payload: RAGRequest):
    request_counter.add(1)

    with tracer.start_as_current_span("rag-handler") as span:
        span.set_attribute("rag.query", payload.query)

        with tracer.start_as_current_span("embed"):
            query_vec = embed_query(payload.query)

        with tracer.start_as_current_span("retrieve"):
            docs = search_vector_db(query_vec)

        with tracer.start_as_current_span("generate"):
            answer = generate_answer(docs, payload.query)

        return {"answer": answer, "documents": docs}
