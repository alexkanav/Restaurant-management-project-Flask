from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db, safe_commit, logger


class Category(db.Model):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(db.String(20), unique=True)
    names: Mapped[dict[str]] = mapped_column(JSON)

    def __repr__(self):
        return f"<Category {self.category}>"


class Price(db.Model):
    __tablename__ = 'prices'

    id: Mapped[int] = mapped_column(primary_key=True)
    price: Mapped[dict[str, int]] = mapped_column(JSON)


class Statistics(db.Model):
    __tablename__ = 'statistics'

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column(db.String(10), unique=True)
    number_users: Mapped[int]
    number_orders: Mapped[int]
    total_sum: Mapped[int]


class Staff(UserMixin, db.Model):
    __tablename__ = 'staff'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(db.String(200))
    email: Mapped[str] = mapped_column(db.String(100), unique=True)
    password_hash: Mapped[str] = mapped_column(db.String(100))

    def __repr__(self):
        return f"<Staff {self.email}>"

    @property
    def password(self):
        raise AttributeError("Password is write-only.")

    @password.setter
    def password(self, plain_password: str):
        self.password_hash = generate_password_hash(plain_password, method='pbkdf2:sha256')

    def check_password(self, password_input: str) -> bool:
        return check_password_hash(self.password_hash, password_input)

    @classmethod
    def add_user(cls, name: str, email: str, password: str):
        new_user = cls(username=name, email=email)
        new_user.password = password
        db.session.add(new_user)
        if not safe_commit():
            logger.error("Could not add staff.")
            return False
        return True

