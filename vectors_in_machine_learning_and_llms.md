# What Are Vectors in Machine Learning and LLMs

## ✅ What is a Vector?

A **vector** is a **list of numbers** that describes something in a mathematical space.

In machine learning and LLMs, vectors represent words, sentences, images, or other data **as numerical forms** that models can process.

---

## ✅ Real-World Analogy

A vector is like an **address in space**.

Example: A 3D vector could be:

| X | Y | Z |
|---|---|---|
| 3 | 5 | 7 |

This represents a point at (3, 5, 7) in 3D space.

---

## ✅ Example in Language Models

When processing the word `"cat"`:

```
"cat" → [0.12, -0.33, 0.87, 0.44, -0.25, ...]
```

This could be a **300-dimensional vector** or a **4096-dimensional vector**, depending on the model.

---

## ✅ What Do These Numbers Represent?

- They represent learned features of the word or phrase.
- Example: Some values may capture whether the word is an animal, noun, or part of a common phrase.
- **Individual vector values don’t have human-readable meanings** — they’re learned by the model.

---

## ✅ Common Uses of Vectors in LLMs

| Use | Example |
|---|---|
| Word Embeddings | "cat" → [0.1, -0.2, 0.8, ...] |
| Sentence Embeddings | "The cat sat" → [0.5, 0.4, -0.3, ...] |
| Model Parameters | Model weights are stored as vectors |
| Comparing Similarity | Cosine similarity between two vectors |
| Visualization | t-SNE or PCA to reduce dimensions and visualize clusters |

---

## ✅ Vector Math Examples

| Operation | Purpose |
|---|---|
| Cosine Similarity | Check if two vectors represent similar meanings |
| Vector Addition | `vector("king") - vector("man") + vector("woman") ≈ vector("queen")` |
| Dot Product | Basis for attention score calculations |

---

## ✅ Why Vectors Matter in LLMs

Language models don’t "understand" words directly. They work with **patterns of numbers (vectors)**.

All words, sentences, and inputs are **transformed into vectors before being processed** by the model.

---

[Back to Overview](Local%20LLM%20Project%20Overview.md)
