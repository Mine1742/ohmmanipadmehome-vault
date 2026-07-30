# Word Embeddings: Word2Vec, GloVe, and Transformer Embeddings

## ✅ What Are Word Embeddings?

Word embeddings are **numerical vector representations of words**.  
They allow machine learning models to work with words as numbers while preserving **semantic relationships** (meaning).

---

## ✅ Classic Word Embeddings

### 🔹 Word2Vec

- Created by Google (2013)
- Trains a shallow neural network to predict:
  - **CBOW:** Predict a word from its context
  - **Skip-gram:** Predict context from a word
- Produces **fixed-size vectors** (e.g., 300 dimensions) for each word
- Learns relationships like:
  
  ```
  vector("king") - vector("man") + vector("woman") ≈ vector("queen")
  ```

---

### 🔹 GloVe (Global Vectors)

- Created by Stanford (2014)
- Trains on **word co-occurrence statistics** from a large corpus
- Also creates **fixed-size word vectors**
- Emphasizes **global statistical information** vs. Word2Vec's local context windows

---

## ✅ Limitations of Classic Embeddings

| Limitation | Example |
|---|---|
| Static | `"bank"` has the same vector in "river bank" and "money bank" |
| Word-level only | No sentence-level understanding |
| Can't model rare words | Words not seen during training have no vectors |

---

## ✅ Transformer Embeddings (Modern LLMs)

Transformers (like BERT, GPT, Llama) produce **contextual embeddings**, meaning the embedding for a word **depends on its surrounding context.**

### Example:

| Sentence | Embedding for "bank" |
|---|---|
| "He sat by the river bank." | Contextualized for river meaning |
| "She deposited money at the bank." | Contextualized for financial meaning |

---

### Key Features of Transformer Embeddings

| Feature | Transformers |
|---|---|
| Contextualized | Yes ✅ |
| Dynamic (depends on sentence) | Yes ✅ |
| Handles unknown words | Yes (via subword tokenization) |
| Works at token level | Yes |
| Also produces sentence embeddings | Yes (via pooling) |

---

## ✅ Summary Comparison

| Feature | Word2Vec / GloVe | Transformers |
|---|---|---|
| Type | Static | Contextual |
| Trained on | Co-occurrence / Local context | Self-attention on full sentence |
| Handles ambiguity | ❌ | ✅ |
| Sentence understanding | ❌ | ✅ |
| Modern usage | Rare | Standard |

---

## ✅ Popular Pre-trained Embeddings

| Type | Example |
|---|---|
| Word2Vec | GoogleNews-vectors |
| GloVe | Common Crawl, Wikipedia datasets |
| Transformers | BERT, GPT, Llama, DistilBERT, RoBERTa |

---

[Back to Overview](Local%20LLM%20Project%20Overview.md)
