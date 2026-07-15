import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from .configs import config, Ollama_config
import requests

def get_working_url(urls):
    for url in urls:
        try:
            res = requests.get(f"{url}/api/tags", timeout=2)
            if res.status_code == 200:
                # print(f"✅ Working: {url}")
                return url
        except Exception as e:
            # print(f"❌ Failed: {url}")
            pass
    raise Exception("No working LLM URL found")


def gemini_llm():
    load_dotenv()
    llm = init_chat_model(
        model=config["model"],
        model_provider=config["model_provider"],
        api_key=os.getenv("GEMINI_API_KEY"),
        base_url=config["base_url"]
    )
    return llm

def ollama_llm():
    load_dotenv()
    llm = init_chat_model(
        model=Ollama_config["model"],
        model_provider=Ollama_config["model_provider"],
        api_key=os.getenv("OLLAMA_API_KEY"),
        base_url=get_working_url(Ollama_config["base_url"])
    )
    return llm
if __name__ == "__main__":
    # gemini_llm()
    ollama_llm()

    import logging
    logging.basicConfig(level=logging.INFO)
    logging.info("LLM initialized successfully.")
    