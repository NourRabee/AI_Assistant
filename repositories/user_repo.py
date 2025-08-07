from sqlalchemy.orm import Session

from domain.models import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def save(self, user: User):
        self.db.add(user)
        self.db.commit()

    def update_password(self, user: User, new_hashed_password: str):
        user.hashed_password = new_hashed_password
        self.db.commit()

