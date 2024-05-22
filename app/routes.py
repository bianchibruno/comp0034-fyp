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
    request = Request.query.get_or_404(request_id)
    request_schema.load(request_data, instance=request, partial=True)
    db.session.commit()
    return request_schema.jsonify(request)

@bp.route('/requests/<int:request_id>', methods=['DELETE'])
def delete_request(request_id):
    request = Request.query.get_or_404(request_id)
    db.session.delete(request)
    db.session.commit()
    return jsonify({'message': 'Request deleted'}), 202

def init_app(app):
    app.register_blueprint(bp)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # from .routes import init_app
    # init_app(app)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app