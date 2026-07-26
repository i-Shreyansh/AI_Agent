
from pydantic import BaseModel, Field
import operator
from typing import Optional, Literal, Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages


class ResponseFormat(BaseModel):
    step: Literal["PLAN", "TOOL", "OUTPUT", "ERROR"] 
    content: str = Field(..., description="The optional string content for the step")
    tool: Optional[str] = Field(None, description="The ID of the tool to call.")
    input: Optional[str] = Field(None, description="The input params for the tool")



class State(TypedDict):
    messages: Annotated[list, add_messages]
    # ``operator.add`` preserves earlier plans when a node returns new ones.
    plans: Annotated[list[str], operator.add]
    structured_response: Optional[ResponseFormat]
