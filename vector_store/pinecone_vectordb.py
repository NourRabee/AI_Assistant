from typing import List

from langchain_mistralai import MistralAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document

from pinecone import Pinecone

from core.config import settings


class PineconeStore:
    def __init__(self):
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.index = self.pc.Index(settings.PINECONE_INDEX)
        self.embedding = MistralAIEmbeddings(
            model="mistral-embed",
            api_key=settings.MISTRAL_API_KEY,
        )
        self.vectorstore = PineconeVectorStore(
            index=self.index,
            embedding=self.embedding,
            text_key="text",
            namespace="conv_mem"
        )

    def upsert(self, doc: List[Document], namespace="conv_mem"):
        self.vectorstore.add_documents(doc, namespace=namespace)

    def search(self, prompt, conversation_id, user_id, top_k=5, namespace="conv_mem"):
        print(f"Searching in namespace={namespace} for user_id={user_id}, conversation_id={conversation_id}")

        retriever = self.vectorstore.as_retriever(
            search_kwargs={
                "k": top_k,
                "filter": {
                    "$and": [
                        {"user_id": {"$eq": user_id}},
                        {"conversation_id": {"$eq": conversation_id}}
                    ]
                },
                "namespace": namespace
            }
        )

        return retriever.invoke(prompt)

    def get_text(self, results):
        return [doc.page_content for doc in results]

    def convert_text_to_list_doc(self, text, conversation_id, user_id) -> List[Document]:
        return [
            Document(
                page_content=text,
                metadata={"conversation_id": conversation_id, "user_id": user_id}
            )
        ]
