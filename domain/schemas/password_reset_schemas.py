import re

from pydantic import BaseModel, EmailStr, field_validator


class PasswordResetRequest(BaseModel):
    email: EmailStr


class VerifyPasswordResetToken(BaseModel):
    email: EmailStr
    token: str


class PasswordReset(BaseModel):
    email: EmailStr
    new_password: str

    @field_validator("new_password")
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")

        return v
