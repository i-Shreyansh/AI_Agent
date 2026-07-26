
Config = {
    # "llm": "ollama"
    # "llm": "gemini"
    "llm": "openrouter"
}

geminiConfig = {
    "model": "gemini-2.5-flash",
    "model_provider": "openai",
    "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/"

}
ollamaConfig = {
    # "model": "gemma3:1b",
    "model": "qwen2.5:1.5b",
    "model_provider": "ollama",
    "base_url": ["http://localhost:11434/",
                 "http://ollama_new:11434/", 
                    "http://ollama:11434/"
                 ]
}

openrouterConfig = {
    "model": "google/gemma-4-26b-a4b-it:free",
    "model_provider": "openai",
    "base_url": "https://openrouter.ai/api/v1"
}