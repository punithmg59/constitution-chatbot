from fastapi import APIRouter, HTTPException
from app.schemas import ChatRequest, ChatResponse
from app.services.rag_service import retrieve_context, is_constitution_question
from app.services.llm_service import generate_answer

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        query = request.query.strip()

        if not query:
            raise HTTPException(status_code=400, detail="Empty query")

        # Check if question is about constitution
        if is_constitution_question(query):
            context = retrieve_context(query)
        else:
            context = None  # No constitution context for general questions

        answer = generate_answer(query, context)

        return ChatResponse(query=query, answer=answer)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))