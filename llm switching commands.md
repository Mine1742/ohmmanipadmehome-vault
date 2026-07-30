#llm
# Use local Ollama (free, private)
python main.py --llm-provider ollama --goal "your query"

# Use Claude (best quality)
python main.py --goal "your query"

# Switch providers anytime
$env:LLM_PROVIDER = "ollama"
python main.py --goal "your query"

$env:LLM_PROVIDER = "claude"
python main.py --goal "your query"
