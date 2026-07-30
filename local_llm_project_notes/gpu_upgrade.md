# GPU Upgrade Planning for Local LLMs

## Why Upgrade?

Running larger models (13B and up) or faster inference times usually requires a discrete GPU with more VRAM.

## Recommended GPUs for LLM Workloads

| GPU | VRAM | Notes |
|---|---|---|
| NVIDIA RTX 3060 | 12GB | Budget LLM workloads |
| NVIDIA RTX 4070 / 4080 | 12-16GB | Good balance |
| NVIDIA RTX 4090 | 24GB | High-end |
| AMD GPUs | Varies | Limited support in LLM frameworks (some ROCm support) |

## AMD Warning

Currently, most LLM frameworks (Hugging Face, llama.cpp) are **optimized for NVIDIA CUDA GPUs**.

For AMD GPUs: Research ROCm compatibility before purchase.

[Back to Overview](Local%20LLM%20Project%20Overview.md)
