from flask import Flask, request, jsonify, Blueprint, abort, current_app as app, request, jsonify, make_response
from .schemas import RequestSchema
from app import db, ma
from app.models import Request, User
from marshmallow.exceptions import ValidationError
from datetime import datetime, timedelta
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from .helpers import encode_auth_token, token_required, is_valid_email, requires_role



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
@token_required
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
@token_required
def update_request(request_id):
    request_data = request.get_json()
    request_item = db.session.get(Request, request_id)
    if not request_item:
        return jsonify({'message': 'Request not found'}), 404

    request_schema.load(request_data, instance=request_item, partial=True)
    db.session.commit()
    return jsonify({'message': 'Request updated.', 'data': request_schema.dump(request_item)}), 200


@bp.route('/requests/<int:request_id>', methods=['DELETE'])
@token_required
def delete_request(request_id):
    request = db.session.get(Request, request_id)
    if not request:
        abort(404)
    db.session.delete(request)
    db.session.commit()
    return jsonify({'message': 'Request deleted'}), 202

def init_app(myApp):
    myApp.register_blueprint(bp)

@bp.route('/register', methods=['POST'])
def register():
    post_data = request.get_json()

    # Check if both email and password are present
    if not post_data or 'email' not in post_data or 'password' not in post_data:
        return make_response(jsonify({"message": "Missing email or password"}), 400)

    # Validate the email format
    if not is_valid_email(post_data['email']):
        return make_response(jsonify({"message": "Invalid email format"}), 400)

    # Check if the user already exists
    user = db.session.execute(
        db.select(User).filter_by(email=post_data['email'])
    ).scalar_one_or_none()

    if user:
        return make_response(jsonify({"message": "User already exists. Please Log in."}), 409)

    try:
        user = User(
            email=post_data['email'],
            password=generate_password_hash(post_data['password'])
        )
        db.session.add(user)
        db.session.commit()
        return make_response(jsonify({"message": "Successfully registered."}), 201)

    except Exception as err:
        print(err)
        return make_response(jsonify({"message": "An error occurred. Please try again."}), 500)

@bp.route('/login', methods=['POST'])
def login():
    """Logins in the User and generates a token."""
    auth = request.get_json()

    # Check the email and password are present, if not return a 401 error
    if not auth or not auth.get('email') or not auth.get('password'):
        msg = {'message': 'Missing email or password'}
        return make_response(jsonify(msg), 401)

    # Find the user in the database
    user = db.session.execute(
        db.select(User).filter_by(email=auth.get("email"))
    ).scalar_one_or_none()

    # If the user is not found, or the password is incorrect, return 401 error
    if not user or not user.verify_password(auth.get('password')):
        msg = {'message': 'Incorrect email or password.'}
        return make_response(jsonify(msg), 401)

    # If all OK then create the token
    token = encode_auth_token(user.id)

    # Return the token and the user_id of the logged in user
    return make_response(jsonify({"user_id": user.id, "token": token}), 201)

@bp.route('/secure-data', methods=['GET'])
@token_required
def secure_data():
    return jsonify({'message': 'Access to secure data successful'}), 200

@bp.route('/delete-user/<string:email>', methods=['DELETE'])
@token_required
@requires_role('administrator')
def delete_user(email):
    user_to_delete = User.query.filter_by(email=email).first()
    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404
