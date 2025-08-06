from pydantic import BaseModel, EmailStr


class LogInRequest(BaseModel):
    email: EmailStr
    password: str
