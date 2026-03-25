from fastapi import status, HTTPException
from uuid import UUID

from app.application.services.admin_service import AdminServices
from app.application.exceptions import UserNotAllowError, UserNotFoundError
from app.presentation.schemas.user_schema import UserOut


class AdminController:
    def __init__(self, service: AdminServices):
        self.service = service

    def get_all_users(self, user_id: UUID, role: str):
        try:
            response = self.service.get_all_users(user_id, role)
            return [
                UserOut(
                    user_id=raw.user_id,
                    email=raw.email,
                    username=raw.username,
                    role=raw.role,
                    avatar_url=raw.avatar_url,
                    is_actived=raw.is_actived,
                )
                for raw in response
            ]
        except UserNotAllowError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    def grant_admin(self, admin_id: UUID, role: str, user_id: UUID):
        if role != "ADMIN":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        try:
            return self.service.grant_admin(admin_id, user_id)
        except UserNotAllowError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        except UserNotFoundError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    def lock_user(self, admin_id: UUID, role: str, user_id: UUID):
        if role != "ADMIN":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        try:
            return self.service.lock_user(admin_id, user_id)
        except UserNotAllowError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        except UserNotFoundError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    def unlock_user(self, admin_id: UUID, role: str, user_id: UUID):
        if role != "ADMIN":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        try:
            return self.service.unlock_user(admin_id, user_id)
        except UserNotAllowError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        except UserNotFoundError:
            raise HTTPException(detail="User not found",status_code=status.HTTP_404_NOT_FOUND)
