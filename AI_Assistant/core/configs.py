
Config = {
    # llm: "ollama",
    "llm": "gemini"
}

geminiConfig = {
    "model": "gemini-2.5-flash",
    "model_provider": "openai",
    "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/"

}
ollamaConfig = {
    "model": "gemma3:1b",
    "model_provider": "ollama",
    "base_url": ["http://localhost:11434/",
                 "http://ollama_new:11434/", 
                    "http://ollama:11434/"
                 ]
}