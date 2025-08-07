import uuid

from sqlalchemy.orm import Session

from domain.mappers.user_mapper import UserMapper
from domain.schemas.login_response import LogInResponse
from domain.models import PasswordResetToken
from repositories.password_reset_token import PasswordResetTokenRepository
from repositories.user_repo import UserRepository
from services.email import EmailService
from services.jwt import JwtService
from services.password import PasswordService


class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
        self.user_mapper = UserMapper()
        self.password_Service = PasswordService(db)
        self.jwt_service = JwtService()
        self.password_reset_token_repo = PasswordResetTokenRepository(db)
        self.email_service = EmailService(db)

    def register(self, request):
        if not self.user_repo.get_by_email(request.email):
            request.password = self.password_Service.hashPassword(request.password)
            user = self.user_mapper.signup_request_to_user(request)
            self.user_repo.save(user)

            return self.user_mapper.user_to_signup_response(user)

    def login(self, request):
        user = self.user_repo.get_by_email(request.email)
        if user is None or not self.password_Service.verifyPassword(request.password, user.hashed_password):
            return None

        jwt_token = self.jwt_service.generate_jwt_token(user)

        return LogInResponse(jwt_token=jwt_token, token_type="bearer")

    def create_token(self, user):
        generated_token = PasswordResetToken(
            token=str(uuid.uuid4()),
            user_id=user.id
        )
        self.password_reset_token_repo.save(generated_token)
        return generated_token

    async def request_password_reset(self, request):
        user = self.user_repo.get_by_email(request.email)
        if user:
            existing_token = self.password_reset_token_repo.get_valid_token_by_user_id(user.id)
            if existing_token:
                self.password_reset_token_repo.mark_token_as_used(existing_token)

            generated_token = self.create_token(user)
            await self.email_service.send_reset_email(user.email, generated_token.token)

    def verified_password_reset_token(self, request):
        user = self.user_repo.get_by_email(request.email)
        valid_token = self.password_reset_token_repo.get_valid_token_by_user_id(user.id)
        if user and valid_token and request.token == valid_token.token:
            self.password_reset_token_repo.mark_token_as_used(valid_token)
            return True
        return False

    def reset_password(self, request):
        user = self.user_repo.get_by_email(request.email)

        if not isinstance(request.new_password, str):
            return False, "Password must be string"
        if not self.password_Service.is_password_strong(request.new_password):
            return False, "Password must be strong"

        if self.password_Service.verifyPassword(request.new_password, user.hashed_password):
            return False, "Password reset failed. Please ensure all information is correct and try again."

        new_hashed_password = self.password_Service.hashPassword(request.new_password)
        self.user_repo.update_password(user, new_hashed_password)
        return True, "Your password has been successfully reset. You can now log in with your new password."
