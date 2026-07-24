from pathlib import Path
import sys

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    
from AI_Assistant.core.prompts import SYSTEM_PROMPT
from AI_Assistant.core.agent import State_graph, State
from openai import RateLimitError

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logging.info("App started ✅")

# 
          
# Initial state (with system prompt)
state = {
    "messages": [
        {"role": "system", "content": SYSTEM_PROMPT }
    ]
}

# 🔁 Chat loop
while True:
    query = input("Enter your query 👉 ")

    if query.lower() in ["exit", "quit", "bye"]:
        print("Exiting chat. Goodbye! 👋")
        break

    # ✅ Append user message
    state["messages"].append({
        "role": "user",
        "content": query
    })
    try:
        # Run graph
        state = State_graph().invoke(state)
    except RateLimitError as e:
        logging.error(f"Rate limit exceeded")
        print("Sorry, the service is currently busy. Please try again later.")
        break
        

    # Get last AI response
    print("Response ✅:", state.get("messages")[-1].content)
