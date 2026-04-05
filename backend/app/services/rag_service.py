from app.services.embedding_service import get_embedding
from app.services.loader_service import loader
from app.utils.logger import logger


# =========================
# DETECT CONSTITUTION QUESTIONS
# =========================
def is_constitution_question(query: str) -> bool:
    """Check if the question is related to Indian Constitution"""
    q = query.lower()
    
    constitution_keywords = [
        "constitution", "article", "schedule", "amendment",
        "fundamental rights", "lok sabha", "rajya sabha",
        "president", "parliament", "directive principle",
        "preamble", "republic day", "indian law", "constitutional",
        "voting", "election", "citizenship", "court",
        "supreme court", "high court", "petition", "writ",
        "fundamental duty", "secular", "socialist", "republic"
    ]
    
    for keyword in constitution_keywords:
        if keyword in q:
            return True
    
    # If query is very short (like "hi", "ok", "hello"), it's not constitution
    if len(q.split()) <= 2 and not any(kw in q for kw in constitution_keywords):
        return False
    
    return False


# =========================
# RETRIEVE CONTEXT
# =========================
def retrieve_context(query: str, k: int = 3) -> str:
    try:
        query_embedding = get_embedding(query)
        D, I = loader.index.search(query_embedding, k)

        results = [loader.articles[i] for i in I[0]]

        # 🔥 LIMIT SIZE (IMPORTANT)
        limited_results = [r[:500] for r in results]

        return "\n\n".join(limited_results)

    except Exception as e:
        logger.error(f"RAG error: {e}")
        raise RuntimeError("RAG failed")