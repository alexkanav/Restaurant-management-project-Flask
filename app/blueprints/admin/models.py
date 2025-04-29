from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.extensions import db


class Categories(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(db.String(20), unique=True)
    names: Mapped[dict[str]] = mapped_column(JSON)


class Prices(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    price: Mapped[dict[str, int]] = mapped_column(JSON)


class Statistics(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column(db.String(10), unique=True)
    number_users: Mapped[int]
    number_orders: Mapped[int]
    total_sum: Mapped[int]




