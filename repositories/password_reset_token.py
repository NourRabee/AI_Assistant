from datetime import datetime, timezone

from domain.models import PasswordResetToken
from repositories.base_repo import BaseRepository


class PasswordResetTokenRepository(BaseRepository):

    def get_valid_token_by_user_id(self, user_id):
        now = datetime.now(timezone.utc)
        return (
            self.db.query(PasswordResetToken)
            .filter(
                PasswordResetToken.user_id == user_id,
                PasswordResetToken.is_used == False,
                PasswordResetToken.expires_at > now
            )
            .order_by(PasswordResetToken.created_at.desc())
            .first()
        )

    def mark_token_as_used(self, token: PasswordResetToken):
        token.is_used = True
        self.db.commit()



