from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session

from db_config import get_db
from domain.schemas.message_request import MessageRequest
from services.conversation import ConversationService
from services.llm import LLMService
from services.message import MessageService

router = APIRouter(prefix="/api/conversations")


def get_conv_service(db: Session = Depends(get_db)) -> ConversationService:
    return ConversationService(db)


def get_msg_service(db: Session = Depends(get_db)) -> MessageService:
    return MessageService(db)


def get_llm_service(db: Session = Depends(get_db)) -> LLMService:
    return LLMService(db)


def get_current_user_id(request: Request) -> int:
    if not hasattr(request.state, "user_id"):
        raise HTTPException(status_code=401, detail="User not authenticated")
    return request.state.user_id


@router.post("/")
def create(user_id: int = Depends(get_current_user_id),
           conv_service: ConversationService = Depends(get_conv_service), ):
    conversation_id = conv_service.create(user_id)
    return {"conversation_id": conversation_id}


@router.get("/{conversation_id}")
def get(conversation_id: int, user_id: int = Depends(get_current_user_id),
        conv_service: ConversationService = Depends(get_conv_service),
        ):
    conversation, messages = conv_service.get(user_id, conversation_id)
    return {
        "id": conversation.id,
        "title": conversation.title,
        "messages": [{"id": m.id, "role": m.sender, "content": m.content, "created_at": m.created_at} for m in messages]
    }


@router.post("/{conversation_id}/messages")
def send_message(request: MessageRequest, conversation_id: int, user_id: int = Depends(get_current_user_id),
                 msg_service: MessageService = Depends(get_msg_service),
                 llm_service: LLMService = Depends(get_llm_service)):
    msg_service.create(conversation_id, request.prompt, user_id, is_ai=False)
    llm_response = llm_service.get_response(request.prompt, conversation_id, user_id)
    msg_service.create(conversation_id, llm_response, user_id, is_ai=True)

    return llm_response


