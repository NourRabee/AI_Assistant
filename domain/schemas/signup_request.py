from pydantic import BaseModel, EmailStr


class SignUpRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str
