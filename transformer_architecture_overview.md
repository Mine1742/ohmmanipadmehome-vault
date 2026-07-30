# Transformer Architecture Overview

## ✅ What is the Transformer?

The Transformer is a deep learning model architecture introduced in the paper:  
**"Attention Is All You Need" (Vaswani et al., 2017)**.

It forms the foundation of most modern LLMs (like GPT, BERT, etc).

---

## ✅ High-Level Components of a Transformer

| Component | Purpose |
|---|---|
| Input Embedding | Converts tokens into dense vectors |
| Positional Encoding | Adds position information to token embeddings |
| Encoder Blocks | Processes the input sequence (BERT uses only encoders) |
| Decoder Blocks | Generates outputs (GPT uses only decoders) |
| Multi-Head Self-Attention | Allows model to focus on different parts of the sequence |
| Feed-Forward Network (FFN) | Applies non-linear transformations |
| Layer Normalization | Helps stabilize training |
| Residual Connections | Allows gradient flow and reduces vanishing gradient issues |

---

## ✅ Transformer Block Workflow (Simplified)

For each block (repeated multiple times):

1. **Self-Attention Layer**
2. **Add & Normalize**
3. **Feed Forward Neural Network**
4. **Add & Normalize**

---

## ✅ Difference Between Encoder and Decoder

| Part | Used in | Purpose |
|---|---|---|
| Encoder | BERT, T5 | Reads and encodes input |
| Decoder | GPT, T5 | Generates text based on input |

---

## ✅ Popular Transformer-based LLM Architectures

| Model | Type |
|---|---|
| BERT | Encoder-only |
| GPT (1/2/3/4) | Decoder-only |
| T5 | Encoder-Decoder |
| Llama | Decoder-only |
| DistilGPT2 | Decoder-only |

---

## ✅ Key Transformer Strengths

- **Parallel Processing**: Can process all tokens at once (unlike RNNs)
- **Long-Range Dependencies**: Easily relates distant tokens
- **Scalability**: Can scale to billions of parameters (LLMs)

---

## ✅ Further Reading

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- Hugging Face Transformers documentation: [https://huggingface.co/docs/transformers/index](https://huggingface.co/docs/transformers/index)

---

[Back to Overview](Local%20LLM%20Project%20Overview.md)
