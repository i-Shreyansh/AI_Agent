import os
from dotenv import load_dotenv
load_dotenv()  # load variables from .env
# from langchain.agents import create_agent
from openai import OpenAI
from time import time

gemini_api_key = os.getenv("GEMINI_API_KEY")
client = OpenAI(
    api_key = gemini_api_key,
    base_url = "https://generativelanguage.googleapis.com/v1beta/"
)

start = time()
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    n=1,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Explain to me how AI works"
        }
    ]
)
end = time()
print(response.choices[0].message)
print(f"Time taken: {end - start} seconds")