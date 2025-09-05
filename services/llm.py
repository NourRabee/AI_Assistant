from langchain_groq import ChatGroq
from core.config import settings
from utils.prompts import build_model_prompt
from vector_store.pinecone_vectordb import PineconeStore


class LLMService:
    def __init__(self):
        self.pinecone_vectordb = PineconeStore()

    def llm(self):
        llm = ChatGroq(
            groq_api_key=settings.GROQ_API_KEY,
            model="llama-3.1-8b-instant",
            temperature=0.2,
            max_tokens=1024,
            timeout=60,
            max_retries=3,
        )
        return llm

    def get_response(self, prompt, conversation_id, user_id):
        raw_result = self.pinecone_vectordb.search(prompt, conversation_id, user_id, namespace="conv_mem")
        relevant_docs = self.pinecone_vectordb.get_text(raw_result)

        formatted_prompt = build_model_prompt(prompt, relevant_docs)
        print(formatted_prompt)

        response = self.llm().invoke(formatted_prompt)

        full_text = f"User: {prompt}\nAssistant: {response.content}"
        docs = self.pinecone_vectordb.convert_text_to_list_doc(full_text, conversation_id, user_id)

        self.pinecone_vectordb.upsert(docs, namespace="conv_mem")

        return response.content

    def generate_title(self, first_message: str):
        response = self.llm().invoke([
            {"role": "system", "content": "You are an assistant that generates short conversation titles."},
            {"role": "user",
             "content": f"Generate a concise title (max 5 words) for this conversation: {first_message}"}
        ])

        return response.content.strip()
