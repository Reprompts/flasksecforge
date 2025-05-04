# 🔐 FlaskSecForge – Production‑Ready Flask API Boilerplate Generator

[![PyPI version](https://img.shields.io/pypi/v/flasksecforge.svg)](https://pypi.org/project/flasksecforge/) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)



- **GitHub:** https://github.com/reprompts/flasksecforge  
- **Community:** https://dev.to/repromptsquest  
- **LinkedIn:** https://www.linkedin.com/groups/14631875/


**Quick Start**

1. **Install** the CLI tool:
   ```bash
   pip install flasksecforge
   ```
2. **Generate** a new Flask API project:
   ```bash
   flasksecforge <your_project>
   ```

---

## ✨ Overview & Goals

FlaskSecForge scaffolds a secure, production‑ready Flask REST API with:

- **Environment Configuration** for development & production
- **Structured Logging** & error handling
- **JWT Authentication**, CORS, and input validation
- **Database‑agnostic** support (SQLite, PostgreSQL, MySQL, SQL Server)
- **Modular Blueprints** (Auth, Users, Items)
- **Example Endpoints** (Health check, Signup/Login, User Profile, CRUD)

---

## 📂 Directory Structure

```plaintext
<your_project>/
├── .env                  # Environment variables
├── requirements.txt      # Python dependencies
├── run.py                # Application entry point
├── config.py             # Config classes (Dev/Prod)
├── gunicorn.conf.py      # Production server settings
├── app/                  # Application package
│   ├── __init__.py       # App factory
│   ├── extensions.py     # DB, Migrate, JWT, CORS
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Marshmallow schemas
│   ├── blueprints/       # Blueprint modules
│   │   ├── auth/         # Auth (register/login)
│   │   ├── users/        # Protected user routes
│   │   └── items/        # CRUD sample resource
│   └── utils.py          # Helpers & error handlers
└── logs/                 # Generated log files
```  

> Each folder and file follows a clear separation of concerns, making customization and extension straightforward.

---

## 🔧 Installation & Setup

1. **Create and activate** a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure** your environment variables in `.env`:
   ```dotenv
   FLASK_ENV=development
   SECRET_KEY=<your_secret>
   JWT_SECRET_KEY=<your_jwt_secret>
   DATABASE_URL=sqlite:///data.db  # or your preferred DB URL
   ```

---

## 🚀 Usage

- **Run migrations**:
  ```bash
  flask db init
  flask db migrate
  flask db upgrade
  ```

- **Start locally**:
  ```bash
  flask run
  ```

- **Deploy with Gunicorn**:
  ```bash
  gunicorn -c gunicorn.conf.py run:app
  ```

---

## 📖 Available Endpoints

| Method | Endpoint          | Description             |
| ------ | ----------------- | ----------------------- |
| GET    | `/health`         | Health check            |
| POST   | `/auth/register`  | Register new user       |
| POST   | `/auth/login`     | Obtain JWT token        |
| GET    | `/users/profile`  | Get current user info   |
| GET    | `/items/`         | List all items          |
| POST   | `/items/`         | Create a new item       |
| PUT    | `/items/<id>`     | Update an existing item |
| DELETE | `/items/<id>`     | Delete an item          |

---

## 🛡️ Security & Best Practices

- Keep `SECRET_KEY` and `JWT_SECRET_KEY` confidential
- Use HTTPS in production
- Validate and sanitize all user inputs
- Rotate tokens and secrets regularly

---

## 🤝 Contributing & Support

Pull requests, issues, and feedback are welcome!

