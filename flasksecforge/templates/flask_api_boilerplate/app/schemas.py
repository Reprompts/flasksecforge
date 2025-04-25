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