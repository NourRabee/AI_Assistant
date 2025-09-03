from langchain_groq import ChatGroq
from sqlalchemy.orm import Session

from core.config import settings


class LLMService:
    def __init__(self, db: Session):
        pass

    def llm(self):
        llm = ChatGroq(
            groq_api_key=settings.GROQ_API_KEY,
            model="deepseek-r1-distill-llama-70b",
            temperature=0,
            max_tokens=1024,
            reasoning_format="parsed",
            timeout=60,
            max_retries=3,
        )

        return llm

    def get_response(self, prompt, conversation_id, user_id):
        response = self.llm().invoke(prompt)

        return response.content if hasattr(response, "content") else response

    def generate_title(self, first_message: str):
        response = self.llm().invoke([
            {"role": "system", "content": "You are an assistant that generates short conversation titles."},
            {"role": "user",
             "content": f"Generate a concise title (max 5 words) for this conversation: {first_message}"}
        ])

        return response.content.strip()
