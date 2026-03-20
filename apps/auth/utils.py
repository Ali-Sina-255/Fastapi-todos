from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt  # type: ignore
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from apps.auth.models import User
from apps.config.db import SessionLocal
from apps.config.settings import ALGORITHM, SECRET_KEY

oAuth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


# async def get_current_user(token: Annotated[str, Depends(oAuth2_bearer)]):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

#         username = payload.get("sub")
#         user_id = payload.get("id")

#         if not username or not user_id:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Could not validate user",
#             )

#         return {"username": username, "user_id": user_id}

#     except PyJWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate user",
#         )


def get_current_user(
    token: Annotated[str, Depends(oAuth2_bearer)], db: Session = Depends(get_db)
):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("id")

    user = db.query(User).filter(User.id == user_id).first()
    return user
