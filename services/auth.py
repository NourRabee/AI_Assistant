from sqlalchemy.orm import Session

from domain.mappers.user_mapper import UserMapper
from domain.schemas.login_response import LogInResponse
from repositories.user_repo import UserRepository
from services.jwt import JwtService
from services.password import PasswordService


class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
        self.user_mapper = UserMapper()
        self.password_Service = PasswordService()
        self.jwt_service = JwtService()

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

    # def get_users(self):
    #     users = self.user_repo.get_all()
    #     return users



