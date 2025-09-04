from domain.models import User
from repositories.base_repo import BaseRepository


class UserRepository(BaseRepository):

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def add(self, user: User):
        self.db.add(user)

    def commit(self):
        self.db.commit()

    def update_password(self, user: User, new_hashed_password: str):
        user.hashed_password = new_hashed_password
        self.db.commit()

