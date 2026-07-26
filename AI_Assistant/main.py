from pathlib import Path
import sys

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    
from AI_Assistant.core.prompts import SYSTEM_PROMPT
from AI_Assistant.core.agent import State_graph, State
from openai import RateLimitError
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logging.info("App started ✅")

# 
          
# Initial state (with system prompt)
state = {
    "messages": [SystemMessage(content=SYSTEM_PROMPT)],
    "plans": [],
}

graph = State_graph()

# 🔁 Chat loop
while True:
    query = input("Enter your query👉 : ")

    if query.lower() in ["exit", "quit", "bye"]:
        print("Exiting chat. Goodbye! 👋")
        break

    # ✅ Append user message
    state["messages"].append(HumanMessage(content= query))
    

 
    
    while True:
        state = graph.invoke(state)
        response = state["structured_response"]


        if response.step == "OUTPUT":
            print(f"Answer🤖 : {response.content}")
            print(f"Plan history🧠 : {state['plans']}")
            break  # finish this query, return to input()

        if response.step == "PLAN":
            print(f"Thinking🧠 : {response.content}")
            state["messages"].append(
                HumanMessage(
                    content="Continue from your plan. If you have enough information, "
                            "return step='OUTPUT' with the final answer."
                )
            )

        elif response.step == "ERROR":
            print("Oops something went wrong! 🫢")
            break

        elif response.step == "TOOL":
            print("Tool execution is not implemented yet.")
            break
        
    print(state)
