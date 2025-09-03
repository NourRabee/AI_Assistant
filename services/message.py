from sqlalchemy.orm import Session

from domain.models import Message
from repositories.conversation import ConversationRepository
from repositories.message import MessageRepository
from services.conversation import ConversationService
from services.llm import LLMService


class MessageService:
    def __init__(self, db: Session):
        self.msg_repository = MessageRepository(db)
        self.conv_service = ConversationService(db)
        self.conv_repository = ConversationRepository(db)
        self.llm_service = LLMService(db)

    def create(self, conversation_id, prompt, user_id, is_ai):
        conversation, messages = self.conv_service.get(user_id, conversation_id)
        if not conversation:
            return False

        if not messages:
            title = self.llm_service.generate_title(prompt)
            conversation.title = title
            self.conv_repository.save(conversation)

        sender = "ai" if is_ai else "user"
        message = Message(conv_id=conversation.id, sender=sender, content=prompt)
        self.msg_repository.save(message)
        self.conv_service.update_last_activity(conversation)

        return True



