from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from backend.data.database import Base
from datetime import datetime

# class User(Base):
#     __tablename__ = "users"

#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     name: Mapped[str] = mapped_column(String(100))
#     email: Mapped[str] = mapped_column(String(200), unique=True)
#     password: Mapped[str] = mapped_column(String(100))


class Valentine(Base):
    __tablename__ = "valentine"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    author: Mapped[str] = mapped_column(String(35))
    text: Mapped[str] = mapped_column(String(1000))
    recipient_id: Mapped[int] = mapped_column(Integer)
    dispatch_date: Mapped[datetime] = mapped_column(DateTime)