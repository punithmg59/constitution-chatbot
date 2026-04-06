from pydantic import BaseModel, Field

# ==================== CHAT SCHEMAS ====================

class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1)

class ChatResponse(BaseModel):
    query: str
    answer: str