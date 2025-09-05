from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db_config import get_db
from domain.schemas.message_request import MessageRequest
from domain.schemas.update_conv_title import UpdateConversationTitle
from services.conversation import ConversationService
from services.llm import LLMService
from services.message import MessageService

router = APIRouter(prefix="/api/conversations")


def get_conv_service(db: Session = Depends(get_db)) -> ConversationService:
    return ConversationService(db)


def get_msg_service(db: Session = Depends(get_db)) -> MessageService:
    return MessageService(db)


llm_service = LLMService()


def get_current_user_id(request: Request) -> int:
    if not hasattr(request.state, "user_id"):
        raise HTTPException(status_code=401, detail="User not authenticated")
    return request.state.user_id


@router.post("/")
def create(user_id: int = Depends(get_current_user_id),
           conv_service: ConversationService = Depends(get_conv_service)):
    conversation_id = conv_service.create(user_id)
    return {"conversation_id": conversation_id}


@router.get("/{conversation_id}")
def get(conversation_id: int, user_id: int = Depends(get_current_user_id),
        conv_service: ConversationService = Depends(get_conv_service),
        ):
    conversation, messages = conv_service.get_with_messages(user_id, conversation_id)
    return {
        "id": conversation.id,
        "title": conversation.title,
        "messages": [{"id": m.id, "role": m.sender, "content": m.content, "created_at": m.created_at} for m in messages]
    }


@router.post("/{conversation_id}/messages")
def send_message(request: MessageRequest, conversation_id: int, user_id: int = Depends(get_current_user_id),
                 msg_service: MessageService = Depends(get_msg_service)):
    msg_service.create(conversation_id, request.prompt, user_id, "user", commit=False)
    llm_response = llm_service.get_response(request.prompt, str(conversation_id), str(user_id))
    msg_service.create(conversation_id, llm_response, user_id, "assistant")

    return llm_response


@router.patch("/{conversation_id}/title")
def update_title(request: UpdateConversationTitle, conversation_id: int, user_id: int = Depends(get_current_user_id),
                 conv_service: ConversationService = Depends(get_conv_service)):
    updated_conversation = conv_service.update_title(conversation_id, user_id, request.title)

    if not updated_conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")

    return {"id": updated_conversation.id, "title": updated_conversation.title}
