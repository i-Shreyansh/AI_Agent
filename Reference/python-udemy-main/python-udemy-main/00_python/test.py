from typing import List, Optional
from pydantic import BaseModel, Field

class User(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    age: Optional[int] = Field(None, gt=0)

user = User(id=1, name="Alice", email="alice@example.com", age=30)
print(user)