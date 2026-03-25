from fastapi import status, HTTPException, UploadFile
from uuid import UUID, uuid4
import os
import shutil
from pathlib import Path
from PIL import Image
from io import BytesIO

from app.domain.exceptions.auth_exceptions import (
    AccountNotFoundError,
    EmailAlreadyExistsError,
)
from app.application.services.user_service import UserServices
from app.application.dtos.user_dto import DTOUpdateUserInput
from app.presentation.schemas.user_schema import UpdateUserInput, UserOut

BASE_DIR = Path(__file__).resolve().parents[2]
PUBLIC_DIR = BASE_DIR / "public"
TEMP_DIR = PUBLIC_DIR / "temp"
AVATARS_DIR = PUBLIC_DIR / "avatars"

TEMP_DIR.mkdir(parents=True, exist_ok=True)
AVATARS_DIR.mkdir(parents=True, exist_ok=True)

MAX_SIZE = (512, 512)
QUALITY = 85


class UserController:
    def __init__(self, service: UserServices):
        self.service = service

    def get_access_user(self, access_token: str):
        try:
            user = self.service.get_me(access_token)
            return UserOut(
                user_id=user.user_id,
                email=user.email,
                username=user.username,
                role=user.role,
                avatar_url=user.avatar_url,
                login_method=user.login_method,
            )
        except AccountNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    def upload_temp_avatar(self, file: UploadFile):
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File phải là kiểu ảnh")

        filename = f"{uuid4()}{os.path.splitext(file.filename)[1]}"
        file_path = TEMP_DIR / filename

        try:
            image = Image.open(file.file)

            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")

            image.thumbnail(MAX_SIZE)

            image.save(
                file_path,
                format="JPEG",
                quality=QUALITY,
                optimize=True,
                progressive=True,
            )

            return f"/static/temp/{filename}"
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Failed to upload temp file")

    def update_me(self, user_id: UUID, payload: UpdateUserInput):
        if payload.avatar_url and "/static/temp/" in payload.avatar_url:
            try:
                filename = os.path.basename(payload.avatar_url)

                source_path = TEMP_DIR / filename
                dest_path = AVATARS_DIR / filename

                if source_path.exists():
                    shutil.move(str(source_path), str(dest_path))
                    payload.avatar_url = f"/static/avatars/{filename}"
            except Exception as e:
                print(f"Lỗi khi di chuyển file: {e}")
        try:
            return self.service.update_me(
                user_id,
                DTOUpdateUserInput(
                    username=payload.username,
                    email=payload.email,
                    role=payload.role,
                    avatar_url=payload.avatar_url,
                ),
            )
        except EmailAlreadyExistsError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
