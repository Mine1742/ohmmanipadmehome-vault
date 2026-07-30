# PyTorch Setup (For Hugging Face Models)

You received the following error in Jupyter Notebook:

```
ImportError: AutoModelForCausalLM requires the PyTorch library but it was not found in your environment.
```

## How to Fix

### If using pip:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### If using conda:

```bash
conda install pytorch torchvision torchaudio cpuonly -c pytorch
```

## Verify PyTorch Installation

```python
import torch
print(torch.__version__)
print(torch.cuda.is_available())  # Should be False (no NVIDIA GPU)
```

[Back to Overview](Local%20LLM%20Project%20Overview.md)
