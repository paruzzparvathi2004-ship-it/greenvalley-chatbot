import os, re
from groq import Groq
from ..rag.vectorstore import retrieve

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a helpful assistant for GreenValley University.
Answer ONLY using the context provided below.
If the answer is not in the context, say: "I'm sorry, I can only answer questions related to GreenValley University. Please contact admissions@greenvalley.edu for more help."
Do NOT use outside knowledge. Be friendly and concise."""

def get_chat_response(question: str, context_chunks: list) -> str:
    context = "\n\n".join(context_chunks)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ],
        max_tokens=512
    )
    return response.choices[0].message.content

def extract_app_id(text: str):
    match = re.search(r'\bAPP\d{3,}\b', text.upper())
    return match.group(0) if match else None
