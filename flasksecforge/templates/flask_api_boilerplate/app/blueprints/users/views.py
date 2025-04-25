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