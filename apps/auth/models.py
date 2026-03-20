from psycopg import Column
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from apps.config.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)

    owner_id = Column(Integer, ForeignKey("users.id"))
