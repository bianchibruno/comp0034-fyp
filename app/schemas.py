from flask_marshmallow import Marshmallow
from app import ma, db
from .models import User, Request

class RequestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Request
        load_instance = True
        sqla_session = db.session
        include_relationships = True
        include_fk = True

