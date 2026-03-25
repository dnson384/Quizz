import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from uuid6 import uuid7
from passlib.context import CryptContext
from typing import Dict, Any
from datetime import datetime, timezone, timedelta
from fastapi import status, HTTPException

from app.application.abstractions.security_abstraction import ISecurityService
from app.infrastructure.config.setting import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SecurityServiceImpl(ISecurityService):
    def hash_password(self, plain_password: str) -> str:
        return pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, payload: Dict[str, Any]) -> str:
        encoded_payload = payload.copy()

        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
        issued_at = datetime.now(timezone.utc)

        encoded_payload.update(
            {"exp": int(expire.timestamp()), "iat": int(issued_at.timestamp())}
        )

        encoded_jwt = jwt.encode(
            encoded_payload, settings.JWT_SECRET, algorithm="HS256"
        )
        return encoded_jwt

    def decode_access_token(self, token: str) -> Dict[str, Any]:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ hoặc đã hết hạn",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
            return payload
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token đã hết hạn",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token không hợp lệ (Chữ ký sai)",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception:
            raise credentials_exception

    def create_refresh_token(self, payload: Dict[str, Any]) -> str:
        encoded_jwt = jwt.encode(payload, settings.JWT_REFRESH, algorithm="HS256")
        return encoded_jwt

    def decode_refresh_token(self, token: str) -> Dict[str, Any]:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ hoặc đã hết hạn",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, settings.JWT_REFRESH, algorithms=["HS256"])
            return payload
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token đã hết hạn",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token không hợp lệ (Chữ ký sai)",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception:
            raise credentials_exception
