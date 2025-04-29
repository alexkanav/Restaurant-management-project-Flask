from app import create_app
from app.extensions import db

from config import HOST

app = create_app()

# create db
# with app.app_context():
#     db.create_all()


if __name__ == '__main__':
    app.run(HOST, 80, debug=False)
