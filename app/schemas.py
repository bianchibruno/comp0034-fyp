from flask_marshmallow import Marshmallow
from app import ma, db
from .models import User, Request

class RequestSchema(ma.SQLAlchemyAutoSchema):
    """
    Marshmallow schema for serializing and deserializing Request objects.
    This schema automatically generates fields corresponding to the Request model.
    It supports both loading and dumping, allowing for easy conversion between JSON and SQLAlchemy models.
    """

    class Meta:
        model = Request  # Specify the SQLAlchemy model
        load_instance = True  # Deserialize to model instances rather than simple dicts
        sqla_session = db.session  # Provide SQLAlchemy session; required for serialization
        include_relationships = True  # Include foreign key relationships
        include_fk = True  # Explicitly include foreign keys in the serialized output

