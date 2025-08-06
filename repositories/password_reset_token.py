from sqlalchemy.orm import Session

from models.password_reset_token import PasswordResetToken


class PasswordResetTokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, token: PasswordResetToken):
        self.db.add(token)
        self.db.commit()
