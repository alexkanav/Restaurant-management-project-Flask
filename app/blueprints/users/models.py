from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import DateTime, JSON

from app.extensions import db


class Users(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(unique=True)
    sessions: Mapped[int] = mapped_column(default=0)
    total_sum: Mapped[int] = mapped_column(default=0)


class Dishes(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    dish_code: Mapped[str] = mapped_column(unique=True)
    dish_name: Mapped[str] = mapped_column(db.String(20), unique=True)
    name_ua: Mapped[str] = mapped_column(db.String(20))
    describe: Mapped[str] = mapped_column(db.String(300))
    image_link: Mapped[str] = mapped_column(db.String(50))
    views: Mapped[int] = mapped_column(default=0)
    likes: Mapped[int] = mapped_column(default=0)


class Orders(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[str] = mapped_column(db.String(20), default=datetime.today().strftime("%d-%m-%Y %H:%M"))
    completed: Mapped[str] = mapped_column(db.String(5), default='No')
    user_id: Mapped[int]
    table_number: Mapped[int] = mapped_column(nullable=True)
    order_sum: Mapped[int]
    order: Mapped[dict[str, int]] = mapped_column(JSON)


class Comments(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(unique=True)
    user_name: Mapped[str] = mapped_column(db.String(20))
    comment_date_time: Mapped[str] = mapped_column(db.String(10), default=datetime.today().strftime("%d-%m-%Y %H:%M"))
    comment_text: Mapped[str] = mapped_column(db.String(200))

