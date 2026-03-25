from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone

from app.infrastructure.database.connection import Base


class RefreshTokenModel(Base):
    __tablename__ = "refresh_tokens"

    jti = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    issued_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    user = relationship("UserModel", back_populates="refresh_token")
