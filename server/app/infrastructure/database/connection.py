from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator

from app.infrastructure.config.setting import settings

# Tạo engine
engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)

# Tạo session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base model
Base = declarative_base()


# hàm dependency injection
def get_db() -> Generator:
    db = SessionLocal()
    try:
        # 'yield' cung cấp session cho request
        yield db
    finally:
        # đảm bảo session được đóng
        db.close()
