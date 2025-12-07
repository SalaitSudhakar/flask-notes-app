# 📝 Flask Notes App

A clean and lightweight **note-taking web app** built with Flask.  
Includes user authentication and full CRUD for notes.  
Designed to be simple, readable, and easy to extend — great for beginners and recruiters reviewing your work.

---

## 🚀 Features

- 🔐 User signup, login, logout
- 🗒️ Create, edit, delete notes
- 🎨 Clean UI (HTML, Jinja2, custom CSS)
- 🗂️ Simple and scalable Flask project structure
- ⚡ Built with best practices (app factory, blueprints, SQLAlchemy)

---

## 🧰 Tech Stack

- **Backend:** Flask, Flask-Login, SQLAlchemy
- **Database:** SQLite (default)
- **Frontend:** HTML (Jinja2), CSS, JavaScript
- **Environment:** Python 3.8+

---

## 📂 Project Structure

Root-level key files and folders:

- main.py : Application entrypoint (runs the Flask app).

- website/ : Flask application package.

- **init**.py : Application factory / app initialization.

- auth.py : Authentication routes and helpers.

- models.py : Database models (notes, users, etc.).

- views.py : Main views for notes and pages.

- templates/ : Jinja2 templates (base.html, home.html, login.html, signup.html).

- static/ : Static assets (style.css, index.js).

---

## ⚡ Quick Start

### 1️⃣ Clone the project

```bash
git clone <repo-url>
cd flask-notes-app

```

### 2️⃣ Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Create a .env file in the project root

```bash
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///database.db
FLASK_ENV=development
DEBUG=True
```

### 5️⃣ Initialize the database

```bash
python -c "from website import db, create_app; app = create_app(); app.app_context().push(); db.create_all()"

```

### 6️⃣ Run the application

```bash
flask run

```

### Open in browser

👉 <http://127.0.0.1:5000>

### 📜 License

This project includes a LICENSE file — follow its terms for reuse.
