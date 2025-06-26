
![image](https://github.com/user-attachments/assets/08442724-0391-4ce7-800c-c5e999fa1bcf)


**vLLM** is a high-performance, user-friendly library for serving and running inference on large language models (LLMs).

Originally built by the **Sky Computing Lab at UC Berkeley**

### Why vLLM is Fast

vLLM is designed for **state-of-the-art inference speed** and efficiency through:

* Industry-leading serving throughput
* Memory-efficient **PagedAttention** for managing attention keys and values
* **Continuous batching** of incoming requests
* Fast execution using **CUDA/HIP graph optimization**
* Support for multiple **quantization methods**: GPTQ, AWQ, INT4, INT8, FP8
* Optimized CUDA kernels, including integration with **FlashAttention** and **FlashInfer**
* Advanced techniques like **speculative decoding** and **chunked prefill**

---

### Why vLLM is Flexible

vLLM supports a wide range of features to make deployment and scaling easy:

* Compatible with popular **HuggingFace models**
* High-throughput serving with **multiple decoding strategies** (e.g., parallel sampling, beam search)
* Support for **tensor and pipeline parallelism** for distributed inference
* **Streaming output** support for real-time applications
* **OpenAI-compatible API** for easy integration
* Hardware support for **NVIDIA GPUs**, **AMD/Intel CPUs and GPUs**, **TPUs**, **IBM Power**, and **AWS Trainium/Inferentia**
* Features like **prefix caching** and **multi-LoRA** support for efficient fine-tuning

---

## Deployment

You can deploy an LLM using the **vLLM** library in several ways, depending on your use case, infrastructure, and desired level of control. Here are the **most common and supported deployment methods**:

---

### 🧠 1. **Standalone Server (OpenAI-Compatible REST API)**

Run the vLLM model server with a simple CLI command, exposing an OpenAI-compatible server.

```sh
vllm serve Qwen/Qwen2.5-1.5B-Instruct
```

```sh
curl http://localhost:8000/v1/models
```

---

### 2. **Dockerized Deployment**

Package and run vLLM in a container (e.g., via Docker or Kubernetes).

```sh
docker run --gpus all -p 8000:8000 --rm \
  vllm/vllm-openai:v0.6.3 \
  --model ibm-granite/granite-3.2-2b-instruct
```

```sh
curl http://localhost:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ibm-granite/granite-3.2-2b-instruct",
    "prompt": "What is the capital of France?",
    "max_tokens": 50,
    "temperature": 0.7
  }'
```

---

### 3. **Kubernetes/Containers with GPU Scheduling**

Deploy vLLM in a Kubernetes cluster using Helm, Kustomize, or raw manifests.

---

### 4. **Embedded Inside a Python Application**

Use vLLM as a Python library to directly run inference in your application:

```python
from vllm import LLM, SamplingParams

llm = LLM(model="facebook/opt-125m")
outputs = llm.generate(["Hello, how are you?"], SamplingParams())
```
---

### 5. **Integrated with Model Serving Platforms**

Deploy vLLM as part of a model server framework like:

* **KServe** (Kubernetes-native model serving)
* **TorchServe** (custom handler for vLLM)
* **Ray Serve** (for scaling across nodes)
* **MLflow** or **Watsonx.ai** (with wrapper containers)

---

### 6. **Distributed Inference Across Multiple GPUs/Nodes**

vLLM supports:

* **Tensor parallelism**
* **Pipeline parallelism**
* **Model sharding**

Useful when:

* Model size exceeds one GPU
* You want to scale throughput across hardware

---

### Summary Table

| Deployment Method                   | Use Case                      | Pros                               |
| ----------------------------------- | ----------------------------- | ---------------------------------- |
| Standalone API Server               | REST-based apps               | Easy, OpenAI-compatible            |
| Docker                              | Cloud-native setups           | Reproducible, portable             |
| Kubernetes                          | Scalable production workloads | Autoscaling, GPU scheduling        |
| Embedded in Python                  | Research & internal tools     | Max control, direct usage          |
| Custom API / gRPC                   | Service architecture          | Flexible, secure                   |
| Integrated with RAG / agent systems | Chatbots, search              | Plug-and-play with LangChain, etc. |
| Model Serving Platforms             | MLOps integration             | Scalable, ML lifecycle support     |
| Multi-GPU / Distributed Inference   | Large models                  | Efficient hardware utilization     |

---
