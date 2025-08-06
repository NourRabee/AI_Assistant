from domain.schemas.signup_request import SignUpRequest
from domain.schemas.signup_response import SignUpResponse
from models import User


class UserMapper:
    def signup_request_to_user(self, request: SignUpRequest) -> User:
        return User(full_name=request.full_name, email=request.email, hashed_password=request.password)

    def user_to_signup_response(self, user: User) -> SignUpResponse:
        return SignUpResponse(id=user.id)
