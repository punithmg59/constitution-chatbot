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
            raise ValueError("GROQ_API_KEY is missing")

        client = Groq(api_key=settings.GROQ_API_KEY)
        logger.info("✅ Groq client initialized")

    except Exception as e:
        logger.error(f"❌ Groq init error: {e}")
        raise RuntimeError("Groq initialization failed")


# =========================
# INTENT DETECTION
# =========================
def detect_intent(query: str):
    q = query.lower()

    if any(w in q for w in ["what is", "define", "meaning"]):
        return "short"

    if any(w in q for w in ["explain", "why", "how"]):
        return "medium"

    if any(w in q for w in ["compare", "difference"]):
        return "structured"

    return "medium"


# =========================
# PROMPT BUILDER
# =========================
def build_prompt(query: str, context: str, intent: str):

    base_rules = """
You are an expert Indian Constitution assistant.

Strict Rules:
- Do NOT give long answers unless needed
- Be precise and structured
- Avoid repeating context
- Do NOT hallucinate outside context
"""

    if intent == "short":
        style = """
Give ONLY a short answer (1-2 lines).
No explanation unless necessary.
"""

    elif intent == "medium":
        style = """
Give:
- 1 short answer
- Then 2-3 bullet points explanation
"""

    elif intent == "structured":
        style = """
Give structured answer using bullet points.
Compare clearly if needed.
"""

    else:
        style = "Give a clear answer."

    return f"""
{base_rules}

{style}

Context:
{context}

Question:
{query}

Answer:
"""


# =========================
# GENERATE ANSWER
# =========================
def generate_answer(query: str, context: str) -> str:
    try:
        if client is None:
            raise RuntimeError("Groq client not initialized")

        if not query.strip():
            raise ValueError("Query is empty")

        if not context.strip():
            raise ValueError("Context is empty")

        # 🔥 Limit context
        context = context[:1200]

        # 🔥 Detect intent
        intent = detect_intent(query)

        # 🔥 Build dynamic prompt
        prompt = build_prompt(query, context, intent)

        # 🔥 Dynamic token control
        if intent == "short":
            max_tokens = 80
        elif intent == "medium":
            max_tokens = 180
        else:
            max_tokens = 250

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,   # 🔥 more consistent
            max_tokens=max_tokens
        )

        if not response or not response.choices:
            raise ValueError("Empty LLM response")

        answer = response.choices[0].message.content

        if not answer:
            raise ValueError("No content in response")

        return answer.strip()

    except Exception as e:
        logger.error(f"❌ LLM error: {e}")
        return "Sorry, I couldn't generate a proper answer. Please try again."