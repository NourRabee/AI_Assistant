from domain.models import Conversation, Message
from repositories.base_repo import BaseRepository


class ConversationRepository(BaseRepository):

    def get_messages(self, user_id: int, conversation_id: int):
        conversation = self.db.query(Conversation).filter_by(id=conversation_id, user_id=user_id).first()
        if not conversation:
            return None, []

        messages = self.db.query(Message).filter_by(conv_id=conversation.id).order_by(Message.created_at).all()

        return conversation, messages

    def get(self, conversation_id: int, user_id: int):
        conversation = self.db.query(Conversation).filter_by(id=conversation_id, user_id=user_id).first()
        return conversation
