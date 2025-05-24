# Restaurant Ordering System (Flask)

This project is a full-featured restaurant ordering system built using the **Flask** web framework.

---
## Features

- Dynamic menu system where dishes can be created, updated, and displayed
- Customer-facing interface to place new orders
- Admin/staff dashboard to process and complete orders
- Order status tracking (e.g., New → In Progress → Completed)
- Form handling using **Flask-WTF**
- User sessions and authentication via **Flask-Login**
- Performance optimization with **Flask-Caching**
- Persistent storage using **Flask-SQLAlchemy**
- Uses **SQLite** by default (easy for local development)
- Supports **PostgreSQL**, **MySQL**, or other databases via SQLAlchemy
- Modular app structure with Blueprints (main, auth)
- CSRF protection & environment variable config support

Ideal for small restaurants, cafes, or educational purposes demonstrating a real-world Flask app structure.

---
## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/alexkanav/Restaurant-management-project-Flask.git
   cd Restaurant-management-project-Flask

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate

3. Install dependencies:
    ```bash
    pip install -r requirements.txt

---
## Running the App
Note: For production deployments, do not use Flask’s built-in development server (flask run).
Instead, deploy Flask behind a production-grade WSGI server (e.g., Gunicorn) combined with a reverse proxy like Nginx.

---
## License
This project is licensed under the MIT License.