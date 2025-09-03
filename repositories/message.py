from sqlalchemy.orm import Session


class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, message):
        self.db.add(message)
        self.db.commit()
