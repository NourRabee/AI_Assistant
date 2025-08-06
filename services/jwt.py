from datetime import datetime, timedelta, UTC
from fastapi import HTTPException

from core.config import settings
import jwt


class JwtService:
    def generate_jwt_token(self, user):
        payload = {
            "sub": str(user.id),
            "email": user.email,
            "exp": datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return token

    def verify_jwt_token(self, request):
        token = self.get_token_from_request(request)
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload

    def get_token_from_request(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

        return auth_header.split(" ")[1]


