from groq import Groq
from app.config import settings
from app.utils.logger import logger


# =========================
# INIT CLIENT
# =========================
client = None

def init_client():
    global client

    try:
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is missing in .env")

        client = Groq(api_key=settings.GROQ_API_KEY)
        logger.info("✅ Groq client initialized")

    except Exception as e:
        logger.error(f"❌ Failed to initialize Groq client: {e}")
        raise RuntimeError("Groq initialization failed")


# =========================
# GENERATE ANSWER
# =========================
def generate_answer(query: str, context: str) -> str:
    try:
        if client is None:
            raise RuntimeError("Groq client not initialized")

        if not query:
            raise ValueError("Query is empty")

        if not context:
            raise ValueError("Context is empty")

        # 🔥 Limit context size (VERY IMPORTANT)
        context = context[:1500]

        prompt = f"""
You are an expert in Indian Constitution.

Use the context to answer.

Context:
{context}

Question:
{query}

Explain clearly in simple words.

Also include:
- full meaning of the article
- real-life interpretation if needed
- not just legal definition
"""
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ✅ stable model
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=300
        )

        # ✅ Validate response
        if not response or not response.choices:
            raise ValueError("Empty response from LLM")

        answer = response.choices[0].message.content

        if not answer:
            raise ValueError("No content in LLM response")

        return answer.strip()

    except Exception as e:
        logger.error(f"❌ LLM error: {e}")

        # return safe response (no crash)
        return "Sorry, I couldn't generate a response. Please try again."