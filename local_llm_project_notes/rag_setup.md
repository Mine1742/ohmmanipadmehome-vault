# Retrieval-Augmented Generation (RAG) Setup

## What is RAG?
RAG combines an LLM with your private files, documents, or databases. The LLM first retrieves relevant data, then generates an answer.

## Basic Workflow

1. **Document Store**: Load your PDFs, Markdown files, etc.
2. **Embedding Model**: Converts text to vector embeddings (e.g., using `sentence-transformers`).
3. **Vector Search**: Retrieve relevant chunks (using FAISS, ChromaDB, etc).
4. **LLM Inference**: Ask the LLM to generate answers using the retrieved chunks.

## Popular RAG Tools

- LangChain
- LlamaIndex
- Haystack

## Windows-Friendly Quick Start

- ChromaDB + LangChain + Ollama

## Example Resources

- [https://python.langchain.com/docs/get_started/introduction](https://python.langchain.com/docs/get_started/introduction)
- [https://github.com/jerryjliu/llama_index](https://github.com/jerryjliu/llama_index)

[Back to Overview](Local%20LLM%20Project%20Overview.md)
