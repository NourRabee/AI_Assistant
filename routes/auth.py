from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from db_config import get_db
from domain.schemas.login_request import LogInRequest
from domain.schemas.signup_request import SignUpRequest
from services.auth import AuthService

router = APIRouter(prefix="/api/auth")


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)


@router.post("/sign_up")
def sign_up(
    request: SignUpRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    user_id = auth_service.register(request)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists."
        )

    return user_id


@router.post("/login")
def login(request: LogInRequest,  auth_service: AuthService = Depends(get_auth_service)):
    jwt_token = auth_service.login(request)
    if jwt_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    return jwt_token


# @router.get("/users")
# def get_users(auth_service: AuthService = Depends(get_auth_service)):
#     users = auth_service.get_users()
#     return users
