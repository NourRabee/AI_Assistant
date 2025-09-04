from pydantic import BaseModel, EmailStr


class LogInRequest(BaseModel):
    email: EmailStr
    password: str


class LogInResponse(BaseModel):
    jwt_token: str
    token_type: str


class SignUpRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str


class SignUpResponse(BaseModel):
    id: int

