# How Is a Learned Query Projection Matrix Created in Transformers?

## ✅ What is the Query Projection Matrix?

The **Query Projection Matrix (`W_Q`)** is a **learnable weight matrix** used to transform a token's embedding into a Query vector during self-attention.

---

## ✅ Step-by-Step: How It’s Created and Learned

### Step 1: Random Initialization

When the Transformer model is first created, the Query projection matrix is initialized with **random values**.

Example shape (for a model with 768-dimensional embeddings):

```
W_Q shape: [768, 768]
```

---

### Step 2: Used in the Forward Pass

For every token embedding (`x`), the Query (`q`) is computed as:

```python
q = x @ W_Q
```

- `x`: The word embedding vector
- `W_Q`: The Query projection matrix
- `@`: Matrix multiplication

This projects the original embedding into a new space designed for comparison with Key vectors.

---

### Step 3: Loss Calculation and Backpropagation

- The model performs its task (e.g., predicting masked tokens).
- It calculates the **loss** (how far off the model's predictions are from the correct answer).
- During **backpropagation**, gradients are computed for all weights, including `W_Q`.

---

### Step 4: Update the Matrix

The weights are updated using **gradient descent:**

```
W_Q ← W_Q - learning_rate * gradient_of_loss_with_respect_to_W_Q
```

This process adjusts the Query matrix to improve the model's attention focus.

---

## ✅ Why Learn the Query Projection?

| Without Learning | With Learning |
|---|---|
| Random projections | Meaningful Query vectors |
| Attention can't focus properly | Model learns what to focus on |
| Poor performance | Improved understanding of context |

---

## ✅ Summary

| Step | What Happens |
|---|---|
| Initialize | Random numbers |
| Forward pass | Multiply embeddings to create Query vectors |
| Train | Adjust weights through backpropagation |
| Result | Queries that help the model focus on relevant words |

---

[Back to Overview](Local%20LLM%20Project%20Overview.md)
