from sqlalchemy.orm import Session

from domain.models import Message
from repositories.base_repo import BaseRepository
from repositories.conversation import ConversationRepository
from services.conversation import ConversationService
from services.llm import LLMService


class MessageService:
    def __init__(self, db: Session):
        self.base_repo = BaseRepository(db)
        self.conv_service = ConversationService(db)
        self.conv_repository = ConversationRepository(db)
        self.llm_service = LLMService(db)

    def create(self, conversation_id, prompt, user_id, sender, commit=True):
        conversation, messages = self.conv_service.get(user_id, conversation_id)
        if not conversation:
            return False

        if not messages:
            title = self.llm_service.generate_title(prompt)
            conversation.title = title
            self.conv_repository.add(conversation)

        message = Message(conv_id=conversation.id, sender=sender, content=prompt)
        self.base_repo.add(message)
        if commit:
            self.conv_service.update_last_activity(conversation)
            self.base_repo.commit()

        return True



