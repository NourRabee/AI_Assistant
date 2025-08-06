from sqlalchemy.orm import Session

from models import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def save(self, user: User):
        self.db.add(user)
        self.db.commit()

    # def get_all(self):
    #     return self.db.query(User).all()
    #


