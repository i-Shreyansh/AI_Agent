import os
from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from .Chatbot import gemini_llm, ollama_llm
from langgraph.graph import StateGraph, START, END
import logging



# print("Initializing 🔃...")
logging.basicConfig(level=logging.INFO)
logging.info("Conection Initializing...")



class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: State):
    # llm = gemini_llm()
    llm = ollama_llm()
    response = llm.invoke(state.get("messages"))
    return {"messages": [response]}



def State_graph():
    # Graph setup
    graph_builder = StateGraph(State)
    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("chatbot", END)

    graph = graph_builder.compile()
    return graph

# if __name__ == "__main__":
    
#     print(State )
    
#     graph = State_graph(State)
#     graph.invoke("Hii")
#     print(State.dump)
    
#     # with open("graph.png", "wb") as f:
#     #     f.write(graph.get_graph().draw_mermaid_png())

