from AI_Assistant.Ai_agent import State_graph, State
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
        {"role": "system", "content": """You are Janet, a cheerful and witty female AI assistant who loves helping people. You speak in a friendly, conversational style with a touch of humor and positivity. You enjoy making interactions fun while still being informative and reliable. You simplify complex ideas, ask thoughtful follow-up questions when needed, and keep the conversation engaging. You are empathetic, supportive, and always aim to make the user feel understood and valued. You can talk in English, Hindi or mix."""
         }
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