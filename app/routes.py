from flask import Flask, request, jsonify, Blueprint
from .schemas import RequestSchema
from . import db, ma
from .models import Request


requests_schema = RequestSchema(many=True)
request_schema = RequestSchema()

bp = Blueprint('api', __name__)

@bp.route('/requests', methods=['GET'])
def get_requests():
    all_requests = Request.query.all()
    return requests_schema.jsonify(all_requests)

@bp.route('/requests/<int:request_id>', methods=['GET'])
def get_request(request_id):
    request = Request.query.get_or_404(request_id)
    return request_schema.jsonify(request)

@bp.route('/requests', methods=['POST'])
def add_request():
    request_data = request.get_json()
    new_request = request_schema.load(request_data)
    db.session.add(new_request)
    db.session.commit()
    return request_schema.jsonify(new_request), 201

@bp.route('/requests/<int:request_id>', methods=['PATCH'])
def update_request(request_id):
    request_data = request.get_json()
    request_item = Request.query.get_or_404(request_id)
    request_schema.load(request_data, instance=request_item, partial=True)
    db.session.commit()
    return request_schema.jsonify(request_item)

@bp.route('/requests/<int:request_id>', methods=['DELETE'])
def delete_request(request_id):
    request = Request.query.get_or_404(request_id)
    db.session.delete(request)
    db.session.commit()
    return jsonify({'message': 'Request deleted'}), 202

def init_app(app):
    app.register_blueprint(bp)
