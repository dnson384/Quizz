import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
# from fastapi.middleware.cors import CORSMiddleware

from app.infrastructure.database.connection import engine, Base

from app.presentation.routers import (
    auth_router,
    search_router,
    user_router,
    course_router,
    practice_test_router,
    admin_router,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR_PATH = os.path.join(BASE_DIR, "public")

Base.metadata.create_all(bind=engine)

app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["GET", "POST"],
#     allow_headers=["Content-Type", "Authorization"],
# )


@app.get("/")
def read_root():
    return {"message": "Server is running at http://127.0.0.1:8000"}


app.mount("/static", StaticFiles(directory=PUBLIC_DIR_PATH), name="public")

app.include_router(auth_router.router, prefix="/api", tags=["AUTHENTICATION"])
app.include_router(search_router.router, prefix="/api", tags=["SEARCH"])
app.include_router(user_router.router, prefix="/api", tags=["USER"])
app.include_router(course_router.router, prefix="/api", tags=["COURSE"])
app.include_router(practice_test_router.router, prefix="/api", tags=["PRACTICETEST"])
app.include_router(admin_router.router, prefix="/api", tags=["ADMIN"])
