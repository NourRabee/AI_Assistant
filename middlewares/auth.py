from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from services.jwt import JwtService

EXCLUDED_PATHS = [
    "/api/auth/sign_up",
    "/api/auth/login",
    "/api/auth/password_reset_request",
    "/api/auth/verify-password-reset-token",
]


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.jwt_service = JwtService()

    async def dispatch(self, request, call_next):
        if any(request.url.path.startswith(path) for path in EXCLUDED_PATHS):
            return await call_next(request)
        try:
            self.jwt_service.verify_jwt_token(request)
            response = await call_next(request)
            return response
        except HTTPException as exc:
            return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)
        except Exception as exc:
            return JSONResponse(content={"detail": f"Error: {str(exc)}"}, status_code=500)
