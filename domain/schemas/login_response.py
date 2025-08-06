from pydantic import BaseModel


class LogInResponse(BaseModel):
    jwt_token: str
    token_type: str
