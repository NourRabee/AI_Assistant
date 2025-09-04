from sqlalchemy.orm import Session
from datetime import datetime, timezone
from domain.models import Conversation
from repositories.conversation import ConversationRepository


class ConversationService:
    def __init__(self, db: Session):
        self.conversation_repository = ConversationRepository(db)

    def create(self, user_id):
        conversation = Conversation(user_id=user_id)
        self.conversation_repository.add(conversation)
        self.conversation_repository.commit()
        return conversation.id

    def get_with_messages(self, user_id, conversation_id):
        conversation, messages = self.conversation_repository.get_messages(user_id, conversation_id)

        return conversation, messages

    def update_last_activity(self, conversation):
        conversation.last_activity = datetime.now(timezone.utc)
        self.conversation_repository.add(conversation)

    def update_title(self, conversation_id, user_id, title):
        conversation = self.conversation_repository.get(conversation_id, user_id)
        if not conversation:
            return False

        conversation.title = title
        self.conversation_repository.add(conversation)
        self.conversation_repository.commit()

        return conversation




