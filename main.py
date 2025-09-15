from fastapi import FastAPI

from middlewares.auth import AuthMiddleware
from routes import auth, conversation, files

app = FastAPI()

app.include_router(auth.router)
app.include_router(files.router)

app.add_middleware(AuthMiddleware)

app.include_router(conversation.router)

