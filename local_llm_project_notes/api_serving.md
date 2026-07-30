# Serving Your Local LLM as an API

## Why Serve LLM as API?
To allow other apps (chatbots, scripts, etc.) to send questions and get LLM responses over HTTP.

## Options

| Tool | Notes |
|---|---|
| Ollama API | Ollama automatically starts a local API on port 11434 |
| llama.cpp server mode | Exposes HTTP endpoints |
| Hugging Face Transformers + FastAPI | Build your own REST API |

## Example: Using Ollama API

```bash
curl http://localhost:11434/api/generate -d '{"model":"llama3","prompt":"Hello!"}'
```

[Back to Overview](Local%20LLM%20Project%20Overview.md)
