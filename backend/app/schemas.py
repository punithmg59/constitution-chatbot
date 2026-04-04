from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    query: str = Field(..., min_length=3)

class ChatResponse(BaseModel):
    query: str
    answer: str