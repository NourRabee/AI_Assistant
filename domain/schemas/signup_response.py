from pydantic import BaseModel


class SignUpResponse(BaseModel):
    id: int
