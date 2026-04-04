from app.services.embedding_service import get_embedding
from app.services.loader_service import loader
from app.utils.logger import logger


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