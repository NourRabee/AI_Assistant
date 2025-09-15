import logging
from fastapi import APIRouter, UploadFile, File, status, HTTPException, Depends
from starlette.responses import JSONResponse

from routes.conversation import get_current_user_id
from services.file import FileService

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api")

file_service = FileService()


@router.post("/conversations/{conversation_id}/files")
def upload_file(conversation_id: int, file: UploadFile = File(...), user_id: int = Depends(get_current_user_id)):
    try:
        if not file:
            raise ValueError("No file provided")

        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)

        if file_size == 0:
            return ValueError("File is empty!")

        if file_size > 50 * 1024 * 1024:
            raise ValueError("File too large (max 50MB)")

        logger.info(f"Uploading {file.filename}, file_size: {file_size} bytes.")

        file_service.store_to_vectorstore(
            file=file,
            conversation_id=str(conversation_id),
            user_id=str(user_id),
            namespace="memory"
        )

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "File uploaded and stored successfully!"}
        )
    except ValueError as ve:
        logger.error(f"Validation error: {str(ve)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except RuntimeError as re:
        logger.error(f"Runtime error: {str(re)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(re)
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Processing error: {str(e)}"
        )
