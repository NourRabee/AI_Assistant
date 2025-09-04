from pydantic import BaseModel


class UpdateConversationTitle(BaseModel):
    title: str
