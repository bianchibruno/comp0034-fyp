from flask import Flask, request, jsonify, Blueprint, abort
from .schemas import RequestSchema
from . import db, ma
from .models import Request
from marshmallow.exceptions import ValidationError

requests_schema = RequestSchema(many=True)
request_schema = RequestSchema()

bp = Blueprint('api', __name__)

@bp.route('/requests', methods=['GET'])
def get_requests():
    # Use the session directly to perform a query
    all_requests = db.session.execute(db.select(Request)).scalars().all()
    return requests_schema.jsonify(all_requests)

@bp.route('/requests/<int:request_id>', methods=['GET'])
def get_request(request_id):
    # Use session.get to fetch the record, or 404 if not found
    request = db.session.get(Request, request_id)
    if not request:
        abort(404)
    return request_schema.jsonify(request)

@bp.route('/requests', methods=['POST'])
def add_request():
    try:
        request_data = request.get_json()
        new_request = request_schema.load(request_data)
        db.session.add(new_request)
        db.session.commit()
        return request_schema.jsonify(new_request), 201
    except ValidationError as err:
        raise


@bp.route('/requests/<int:request_id>', methods=['PATCH'])
def update_request(request_id):
    request_data = request.get_json()
    request_item = db.session.get(Request, request_id)
    if not request_item:
        return jsonify({'message': 'Request not found'}), 404

    request_schema.load(request_data, instance=request_item, partial=True)
    db.session.commit()
    return jsonify({'message': 'Request updated.', 'data': request_schema.dump(request_item)}), 200


@bp.route('/requests/<int:request_id>', methods=['DELETE'])
def delete_request(request_id):
    request = db.session.get(Request, request_id)
    if not request:
        abort(404)
    db.session.delete(request)
    db.session.commit()
    return jsonify({'message': 'Request deleted'}), 202

def init_app(app):
    app.register_blueprint(bp)

@bp.errorhandler(ValidationError)
def handle_marshmallow_validation(error):
    return jsonify(error.messages), 400
