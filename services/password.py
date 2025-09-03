import re

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from repositories.user_repo import UserRepository


class PasswordService:
    def __init__(self, db: Session):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.user_repository = UserRepository(db)

    def hashPassword(self, password):
        return self.pwd_context.hash(password)

    def verifyPassword(self, password, hashed_password):
        return self.pwd_context.verify(password, hashed_password)
