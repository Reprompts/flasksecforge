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