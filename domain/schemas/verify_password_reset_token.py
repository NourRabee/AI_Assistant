from pydantic import BaseModel, EmailStr


class VerifyPasswordResetToken(BaseModel):
    email: EmailStr
    token: str
