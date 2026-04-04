from fastapi import APIRouter, HTTPException
from app.schemas import ChatRequest, ChatResponse
from app.services.rag_service import retrieve_context
from app.services.llm_service import generate_answer

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        query = request.query.strip()

        if not query:
            raise HTTPException(status_code=400, detail="Empty query")

        context = retrieve_context(query)
        answer = generate_answer(query, context)

        return ChatResponse(query=query, answer=answer)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))