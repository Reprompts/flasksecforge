Step-by-Step Tutorial: Production‑Ready Flask API Boilerplate

This guide will walk you through creating a production-ready Flask REST API boilerplate with integrated security, multi-database compatibility, and a suite of endpoints demonstrating common flows (CRUD, authentication, health checks). You can clone and run immediately after installation.

1. Project Overview & Goals

Production‑ready: Configuration for environments, logging, error handling.

Security: JWT authentication, CORS, input validation.

Database‑agnostic: Works with SQLite, PostgreSQL, MySQL, SQL Server, etc. via an environment variable.

Modular structure: Blueprints for separation of concerns.

Example endpoints: Health check, User signup/signin, CRUD for a sample resource (Item).

2. Directory Structure

flask_api_boilerplate/
├── .env                # Environment variables
├── requirements.txt    # Python dependencies
├── run.py              # Entry point
├── config.py           # Configuration classes
├── gunicorn.conf.py    # Gunicorn production settings
├── app/                # Application package
│   ├── __init__.py     # App factory
│   ├── extensions.py   # Initialize extensions (SQLAlchemy, Migrate, JWT, CORS)
│   ├── models.py       # DB models
│   ├── schemas.py      # Marshmallow schemas
│   ├── blueprints/     # All blueprints
│   │   ├── auth/       # Authentication
│   │   │   ├── __init__.py
│   │   │   ├── views.py
│   │   │   └── serializers.py
│   │   ├── users/      # Protected user endpoints
│   │   │   ├── __init__.py
│   │   │   └── views.py
│   │   └── items/      # CRUD sample resource
│   │       ├── __init__.py
│   │       └── views.py
│   └── utils.py        # Helpers (error handlers, validators)
└── logs/               # Log files

3. Requirements & Environment

Python & Virtualenv

python3 -m venv venv
source venv/bin/activate

requirements.txt

Flask>=2.3
Flask-SQLAlchemy
Flask-Migrate
Flask-JWT-Extended
Flask-Cors
python-dotenv
marshmallow
marshmallow-sqlalchemy
gunicorn

Install dependencies

pip install -r requirements.txt

Environment Variables (.env file)

FLASK_ENV=production
SECRET_KEY=replace-with-secure-key
JWT_SECRET_KEY=replace-with-secure-key
DATABASE_URL=sqlite:///data.db  # or postgresql://user:pass@host/db

4. Configuration (config.py)

import os
from dotenv import load_dotenv

load_dotenv()  # read .env

class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True

class ProductionConfig(BaseConfig):
    DEBUG = False
    LOG_LEVEL = 'INFO'

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
}

5. Extensions (app/extensions.py)

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()

6. App Factory (app/__init__.py)

from flask import Flask, jsonify
from .extensions import db, migrate, jwt, cors
from .config import config
from .blueprints.auth.views import auth_bp
from .blueprints.users.views import users_bp
from .blueprints.items.views import items_bp


def create_app(env=None):
    app = Flask(__name__)
    env = env or os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[env])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(items_bp, url_prefix='/items')

    # Health check
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({'status': 'ok'}), 200

    return app

7. Models & Schemas (app/models.py & app/schemas.py)

from .extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255))

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .models import User, Item

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ('password_hash',)

class ItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        load_instance = True

8. Authentication Blueprint (app/blueprints/auth/views.py)

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from ...extensions import db
from ...models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'User exists'}), 409
    user = User(
        username=data['username'],
        password_hash=generate_password_hash(data['password'])
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id, 'username': user.username}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'message': 'Bad credentials'}), 401
    token = create_access_token({'id': user.id})
    return jsonify({'token': token}), 200

9. Protected User Endpoints (app/blueprints/users/views.py)

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ...models import User
from ...schemas import UserSchema

users_bp = Blueprint('users', __name__)
user_schema = UserSchema()

@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()['id']
    user = User.query.get_or_404(user_id)
    return user_schema.jsonify(user), 200

10. CRUD Sample Resource (app/blueprints/items/views.py)

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from ...extensions import db
from ...models import Item
from ...schemas import ItemSchema

items_bp = Blueprint('items', __name__)
item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

@items_bp.route('/', methods=['GET'])
def list_items():
    items = Item.query.all()
    return items_schema.jsonify(items), 200

@items_bp.route('/', methods=['POST'])
@jwt_required()
def create_item():
    data = request.get_json()
    item = item_schema.load(data, session=db.session)
    db.session.add(item)
    db.session.commit()
    return item_schema.jsonify(item), 201

@items_bp.route('/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    data = request.get_json()
    item.name = data.get('name', item.name)
    item.description = data.get('description', item.description)
    db.session.commit()
    return item_schema.jsonify(item), 200

@items_bp.route('/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return '', 204

11. Entry Point (run.py)

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

12. Gunicorn Configuration (gunicorn.conf.py)

# gunicorn.conf.py
bind = '0.0.0.0:8000'
workers = 4
accesslog = 'logs/access.log'
errorlog = 'logs/error.log'
loglevel = 'info'

13. Logging & Error Handling

Flask’s built‑in logger will capture errors; logs write to logs/ via Gunicorn.

Customize error handlers in app/utils.py as needed.

14. Running the App

# Migrate database
export FLASK_ENV=development
flask db init
flask db migrate
flask db upgrade

# Run locally
python run.py

# Production with Gunicorn
gunicorn -c gunicorn.conf.py run:app

15. README.md (Usage Instructions)

# Flask API Boilerplate

This is a production-ready, secure, database-agnostic Flask REST API boilerplate.

## 🚀 Features
- JWT Authentication
- Modular Blueprint Structure
- Compatible with SQLite, PostgreSQL, MySQL, SQL Server
- CRUD Example + Auth + Profile + Healthcheck
- Ready for Production (Gunicorn, Logging, Environment Configs)

## 🧰 How to Use

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd flask_api_boilerplate

2. Setup your environment

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

3. Configure your .env

Set the appropriate DATABASE_URL, SECRET_KEY, and JWT_SECRET_KEY.

4. Migrate and Run

flask db init
flask db migrate
flask db upgrade
python run.py  # or use Gunicorn in production

5. Available Endpoints

Method

Endpoint

Description

GET

/health

Health Check

POST

/auth/register

Register New User

POST

/auth/login

Login & Get JWT Token

GET

/users/profile

Protected User Info

GET

/items/

List Items

POST

/items/

Create Item

PUT

/items/

Update Item

DELETE

/items/

Delete Item

🧩 How to Modify for Your Use

Add more blueprints inside app/blueprints/

Add more models in app/models.py

Use .env to switch databases

Extend auth logic or add roles with flask-jwt-extended

Add custom error handling inside app/utils.py

🛡️ Security Tips

Always keep SECRET_KEY and JWT_SECRET_KEY safe

Enable HTTPS in production

Rotate tokens if needed

Sanitize all inputs if working with raw SQL

🏁 Ready to Deploy

Use Gunicorn:

gunicorn -c gunicorn.conf.py run:app

✅ Contribute or Extend

Fork and make your custom app on top of this base!


---

You now have a fully functional, secure, production-ready Flask API boilerplate compatible with multiple databases.

Feel free to extend with more blueprints, middleware, and custom error handlers as your project grows!
