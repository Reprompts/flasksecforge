import os
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