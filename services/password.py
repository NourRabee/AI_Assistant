from passlib.context import CryptContext


class PasswordService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hashPassword(self, password):
        return self.pwd_context.hash(password)

    def verifyPassword(self, password, hashed_password):
        return self.pwd_context.verify(password, hashed_password)
