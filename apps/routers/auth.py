from typing import Annotated

from fastapi import APIRouter, Depends, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from apps.auth.models import User
from apps.auth.schema import UserSchema
from apps.config.db import SessionLocal

router = APIRouter()
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ================= DEPENDENCY =================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: UserSchema):
    create_user_model = User(
        username=create_user_request.username,
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        is_active=True,
        hashed_password=bcrypt_context.hash(
            create_user_request.password,
        ),
    )
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    return create_user_model


@router.get("/auth")
async def get_user():
    return {"user": "Authenticated User"}
