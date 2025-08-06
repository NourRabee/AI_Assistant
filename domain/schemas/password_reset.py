from pydantic import BaseModel, EmailStr


class PasswordReset(BaseModel):
    email: EmailStr
    new_password: str
