from groq import Groq
from src.config.settings import GROQ_API_KEY, LLM_MODEL

# Singleton client
_client: Groq | None = None

def get_client() -> Groq:
    global _client
    if _client is None:
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not set in .env")
        _client = Groq(api_key=GROQ_API_KEY)
    return _client

def generate_answer(prompt: str) -> str:
    response = get_client().chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": (
                "آپ ایک اسلامیات کے ماہر استاد ہیں۔ اردو میں جواب دیں۔ "
                "صفحہ نمبر ذکر کریں۔ کبھی [1] جیسے markers نہ لکھیں۔"
            )},
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        max_tokens=1024,
    )
    return response.choices[0].message.content.strip()