from flask import Flask

from .blueprints import register_blueprints
from .extensions import cache, db


def create_app(config_object='config.DatabaseConfig'):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.config['CACHE_TYPE'] = 'SimpleCache'
    cache.init_app(app)
    db.init_app(app)
    register_blueprints(app)

    return app


