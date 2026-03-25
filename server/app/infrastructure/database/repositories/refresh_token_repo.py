from sqlalchemy.orm import Session
from uuid import UUID

from app.application.abstractions.refresh_token_abstraction import (
    IRefreshTokenRepository,
)
from app.domain.entities.token.refresh_token_entity import RefreshToken
from app.infrastructure.database.models.token_model import RefreshTokenModel


class RefreshTokenRepository(IRefreshTokenRepository):
    def __init__(self, db: Session):
        self.db = db

    def save_refresh_token(self, payload: RefreshToken):
        db_token = RefreshTokenModel(
            jti=payload.jti,
            user_id=payload.user_id,
            expires_at=payload.expires_at,
            issued_at=payload.issued_at,
        )
        self.db.add(db_token)
        self.db.commit()

    def is_jti_valid(self, jti: UUID) -> bool:
        token = (
            self.db.query(RefreshTokenModel)
            .filter(RefreshTokenModel.jti == jti)
            .first()
        )
        return token is not None

    def revoke_refresh_token(self, jti: UUID) -> bool:
        token = (
            self.db.query(RefreshTokenModel)
            .filter(RefreshTokenModel.jti == jti)
            .first()
        )

        if token:
            self.db.delete(token)
            self.db.commit()
            return True
        return False

    def revoke_all_tokens_for_user(self, user_id: UUID) -> bool:
        num_deleted = (
            self.db.query(RefreshTokenModel)
            .filter(RefreshTokenModel.user_id == user_id)
            .delete()
        )
        self.db.commit()
        return True
