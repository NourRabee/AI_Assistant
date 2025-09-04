from sqlalchemy.orm import Session


class BaseRepository:
    def __init__(self, db: Session):
        self.db = db

    def commit(self):
        try:
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

    def add(self, obj):
        self.db.add(obj)

    def delete(self, obj):
        self.db.delete(obj)
