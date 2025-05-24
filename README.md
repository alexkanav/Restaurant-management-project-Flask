This project is a full-featured restaurant ordering system built using the Flask web framework.

It includes:

- A dynamic menu system where dishes can be created, updated, and displayed
- A customer-facing interface to place new orders
- An admin/staff dashboard to process and complete orders
- Status tracking (e.g., New → In Progress → Completed)
- Form handling using Flask-WTF
- User sessions and authentication via Flask-Login
- Performance optimization with Flask-Caching
- Persistent storage using Flask-SQLAlchemy
- Uses **SQLite** by default (easy for local development)
- Supports **PostgreSQL**, **MySQL**, or other databases via SQLAlchemy

It’s ideal for small restaurants, cafes, or educational use cases to demonstrate real-world Flask application structure with Blueprints and modular design.


Features:
- Modular app with Blueprints (main, auth)
- User authentication with Flask-Login
- Database ORM with Flask-SQLAlchemy
- CSRF protection & forms with Flask-WTF
- Caching support via Flask-Caching
- Environment variable config support


 Installation:
1. Clone the repository
git clone https://github.com/alexkanav/Restaurant-management-project-Flask

2. Create and activate a virtual environment

3. Install dependencies
pip install -r requirements.txt

Running the App:
- For production deployments, you shouldn't use Flask’s built-in development server (flask run). Instead, you should run Flask behind a production-grade WSGI server, often combined with a reverse proxy like Nginx.


License:
This project is licensed under the MIT License.

