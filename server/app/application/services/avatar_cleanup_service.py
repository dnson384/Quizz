from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
PUBLIC_DIR = BASE_DIR / "app" / "public"
TEMP_DIR = PUBLIC_DIR / "temp"
TEMP_TTL_MINUTES = 15


class AvatarCleanupService:
    def cleanup_temp_avatars():
        now = datetime.now()
        expire_time = now - timedelta(minutes=TEMP_TTL_MINUTES)

        for file in TEMP_DIR.iterdir():
            if not file.is_file():
                continue

            created_at = datetime.fromtimestamp(file.stat().st_ctime)

            if created_at < expire_time:
                try:
                    file.unlink()
                    print(f"Deleted temp file: {file.name}")
                except Exception as e:
                    print(f"Failed to delete {file.name}: {e}")
