import os
from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from AI_Assistant.services.llm import gemini_llm, ollama_llm
from langgraph.graph import StateGraph, START, END
from AI_Assistant.core.configs import Config
import logging
from pydantic import BaseModel, Field
from typing import Optional


# print("Initializing 🔃...")
logging.basicConfig(level=logging.INFO)
logging.info("Conection Initializing...")

class ResponseFormat(BaseModel):
    step: str = Field(..., description="The ID of the step. Example: PLAN, OUTPUT, TOOL, etc")
    content: str = Field(..., description="The optional string content for the step")
    tool: Optional[str] = Field(None, description="The ID of the tool to call.")
    input: Optional[str] = Field(None, description="The input params for the tool")



class State(TypedDict):
    messages: Annotated[list, add_messages]
    structured_response : ResponseFormat

def chatbot(state: State):

    def choose_llm():
        if Config["llm"] == "gemini":
            llm = gemini_llm()  
        elif Config["llm"] == "ollama":
            llm = ollama_llm()
        else:
            raise ValueError(f"Invalid LLM specified in Config: {Config['llm']}")
        return llm
    
    llm = choose_llm().with_structured_output(ResponseFormat)
    
    response = llm.invoke(state.get("messages"))
    # return {"messages": [response]}
    return {"structured_response": response}



def State_graph():
    # Graph setup
    graph_builder = StateGraph(State)
    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("chatbot", END)

    graph = graph_builder.compile()
    return graph


    
if __name__ == "__main__":
    state = {
        "messages": [
            {"role": "user", "content": "Calculate 1+2+3...10?"}
        ]
    }

    graph = State_graph()
    result = graph.invoke(state)

    print(result["structured_response"].model_dump())
    print(state)
 