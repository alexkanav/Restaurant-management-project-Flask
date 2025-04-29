from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_caching import Cache


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

cache = Cache()
