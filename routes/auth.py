from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from db_config import get_db
from domain.schemas.login_request import LogInRequest
from domain.schemas.password_reset import PasswordReset
from domain.schemas.password_reset_request import PasswordResetRequest
from domain.schemas.signup_request import SignUpRequest
from domain.schemas.verify_password_reset_token import VerifyPasswordResetToken
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
def login(request: LogInRequest, auth_service: AuthService = Depends(get_auth_service)):
    jwt_token = auth_service.login(request)
    if jwt_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    return jwt_token


@router.post("/password_reset_request")
async def password_reset_request(request: PasswordResetRequest, auth_service: AuthService = Depends(get_auth_service)):
    await auth_service.request_password_reset(request)

    return {
        "message": "A verification code has been sent to your email. Please check your inbox to continue."
    }


@router.post("/verify-password-reset-token")
def verified_password_reset_token(request: VerifyPasswordResetToken,
                                  auth_service: AuthService = Depends(get_auth_service)):
    verified = auth_service.verified_password_reset_token(request)
    if verified:
        return {
            "message": "The verification code is valid. You may now reset your password."
        }
    return {
        "message": "The verification code is invalid or has expired. Please request a new one."
    }


@router.post("/reset-password")
def reset_password(request: PasswordReset, auth_service: AuthService = Depends(get_auth_service)):
    isResetSuccessful = auth_service.reset_password(request)
    if isResetSuccessful:
        return {
            "message": "Your password has been successfully reset. You can now log in with your new password."
        }
    return {
        "message": "This password may have been used before. Try a new one."
    }

