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
You are a helpful and friendly AI assistant.
- Answer ANY type of question naturally and helpfully
- You have knowledge of the Indian Constitution
- If context about Constitution is provided, use it
- If no context is provided, just answer the question normally
- Be conversational and friendly
- For greetings like "hi", "hello", respond naturally
"""

    if context:
        # Constitution-related question with context
        context_section = f"""
Constitution Context:
{context}

---"""
    else:
        # General question without context
        context_section = ""

    if intent == "short":
        style = """
Give a short, direct answer (1-2 sentences).
"""

    elif intent == "medium":
        style = """
Give a natural, helpful answer with brief explanation if needed.
"""

    elif intent == "structured":
        style = """
Give a clear, structured answer.
"""

    else:
        style = "Give a natural, helpful response."

    prompt = f"""{base_rules}

{style}
{context_section}

Question: {query}

Answer:"""

    return prompt


# =========================
# GENERATE ANSWER
# =========================
def generate_answer(query: str, context: str = None) -> str:
    try:
        if client is None:
            raise RuntimeError("Groq client not initialized")

        if not query.strip():
            raise ValueError("Query is empty")

        # 🔥 Limit context if provided
        if context:
            context = context[:1200]

        # 🔥 Detect intent
        intent = detect_intent(query)

        # 🔥 Build dynamic prompt
        prompt = build_prompt(query, context, intent)

        # 🔥 Dynamic token control
        if intent == "short":
            max_tokens = 100
        elif intent == "medium":
            max_tokens = 200
        else:
            max_tokens = 300

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,   # 🔥 More natural and conversational
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