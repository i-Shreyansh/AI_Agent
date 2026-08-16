import asyncio
import json
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from AI_Assistant.services.llm import gemini_llm, ollama_llm, openrouter_llm
from langgraph.graph import StateGraph, START, END
from AI_Assistant.core.configs import Config
from AI_Assistant.utils.schemas import State, ResponseFormat
import logging
from pathlib import Path



# print("Initializing 🔃...")
logging.basicConfig(level=logging.INFO)
logging.info("Conection Initializing...")





async def chatbot(state: State):

    def choose_llm():
        if Config["llm"] == "gemini":
            llm = gemini_llm()  
        elif Config["llm"] == "ollama":
            llm = ollama_llm()
        elif Config["llm"] == "openrouter":
            llm = openrouter_llm()
        else:
            raise ValueError(f"Invalid LLM specified in Config: {Config['llm']}")
        return llm
    
    llm = choose_llm().with_structured_output(ResponseFormat)
    

    # Plans stay out of the visible chat history, but are provided to the LLM
    # as temporary context on the next graph invocation.
    llm_messages = list(state.get("messages", []))
    if state.get("plans"):
        plan_history = "\n".join(
            f"{number}. {plan}"
            for number, plan in enumerate(state["plans"], start=1)
        )
        llm_messages.append(
            SystemMessage(
                content=(
                    "Planning history for this task:\n"
                    f"{plan_history}\n"
                    "Continue from this history and return OUTPUT when ready."
                )
            )
        )

    response = await llm.ainvoke(llm_messages)
 

    result = {"structured_response": response}
    # The reducer on State.plans appends this entry to the existing list.
    if response.step == "PLAN":
        result["plans"] = [response.content]

    # Only final answers become visible assistant messages.
    elif response.step == "OUTPUT":
        result["messages"] = [AIMessage(content=response.content)]
        

    return result



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
            HumanMessage( content =  "Calculate 1+2+3...10?")
        ],
        "plans": [],
    }

    graph = State_graph()
    state = asyncio.run(graph.ainvoke(state))

    # print(result["structured_response"].model_dump())
    # print(state)
    print(state)
    print("\n\n\n")


    
    mess = HumanMessage( content =  "How are you")

    state["messages"].append(mess)
    state = asyncio.run(graph.ainvoke(state))


    # print(result["structured_response"].model_dump())
    # print(state)
    print(state)
    # print(f"\n\n {State}")
