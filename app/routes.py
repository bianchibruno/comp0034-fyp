from flask import Flask, request, jsonify, Blueprint, abort, current_app as app, request, jsonify, make_response
from .schemas import RequestSchema
from app import db, ma
from app.models import Request, User
from marshmallow.exceptions import ValidationError
from datetime import datetime, timedelta
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from .helpers import encode_auth_token, token_required, is_valid_email, requires_role



# Initialize Marshmallow schemas for serialization and deserialization of data
requests_schema = RequestSchema(many=True)
request_schema = RequestSchema()

# Create a Blueprint named 'api'
bp = Blueprint('api', __name__)

@bp.route('/requests', methods=['GET'])
def get_requests():
    # Retrieve all requests from the database and serialize for JSON response
    all_requests = db.session.execute(db.select(Request)).scalars().all()
    return requests_schema.jsonify(all_requests)

@bp.route('/requests/<int:request_id>', methods=['GET'])
def get_request(request_id):
    # Fetch a single request by ID or return 404 if not found
    request = db.session.get(Request, request_id)
    if not request:
        abort(404)
    return request_schema.jsonify(request)

@bp.route('/requests', methods=['POST'])
@token_required  # Require authentication token to access this route
def add_request():
    try:
        request_data = request.get_json()
        new_request = request_schema.load(request_data)
        db.session.add(new_request)
        db.session.commit()
        return request_schema.jsonify(new_request), 201
    except ValidationError as err:
        raise err

@bp.route('/requests/<int:request_id>', methods=['PATCH'])
@token_required  # Require authentication token to access this route
def update_request(request_id):
    request_data = request.get_json()
    request_item = db.session.get(Request, request_id)
    if not request_item:
        return jsonify({'message': 'Request not found'}), 404

    request_schema.load(request_data, instance=request_item, partial=True)
    db.session.commit()
    return jsonify({'message': 'Request updated.', 'data': request_schema.dump(request_item)}), 200

@bp.route('/requests/<int:request_id>', methods=['DELETE'])
@token_required  # Require authentication token to access this route
def delete_request(request_id):
    request = db.session.get(Request, request_id)
    if not request:
        abort(404)
    db.session.delete(request)
    db.session.commit()
    return jsonify({'message': 'Request deleted'}), 202

def init_app(myApp):
    # Register the Blueprint with the Flask application
    myApp.register_blueprint(bp)

@bp.route('/register', methods=['POST'])
def register():
    # Register a new user and hash their password for storage
    post_data = request.get_json()

    # Ensure both email and password are provided
    if not post_data or 'email' not in post_data or 'password' not in post_data:
        return make_response(jsonify({"message": "Missing email or password"}), 400)

    # Validate email format
    if not is_valid_email(post_data['email']):
        return make_response(jsonify({"message": "Invalid email format"}), 400)

    # Check for existing user to avoid duplicates
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
        print(err)  # Log any error for debugging
        return make_response(jsonify({"message": "An error occurred. Please try again."}), 500)

@bp.route('/login', methods=['POST'])
def login():
    # User login and token generation
    auth = request.get_json()

    # Check for presence of email and password
    if not auth or not auth.get('email') or not auth.get('password'):
        msg = {'message': 'Missing email or password'}
        return make_response(jsonify(msg), 401)

    # Verify user and password correctness
    user = db.session.execute(
        db.select(User).filter_by(email=auth.get("email"))
    ).scalar_one_or_none()

    if not user or not user.verify_password(auth.get('password')):
        msg = {'message': 'Incorrect email or password.'}
        return make_response(jsonify(msg), 401)

    # Successful login leads to token generation
    token = encode_auth_token(user.id)
    return make_response(jsonify({"user_id": user.id, "token": token}), 201)

@bp.route('/secure-data', methods=['GET'])
@token_required  # Secure endpoint requiring token authentication
def secure_data():
    # Example of a secure endpoint that provides sensitive data
    return jsonify({'message': 'Access to secure data successful'}), 200

@bp.route('/delete-user/<string:email>', methods=['DELETE'])
@token_required  # Require authentication token to access this route
@requires_role('administrator')  # Require user to be an administrator
def delete_user(email):
    # Delete a user by their email
    user_to_delete = User.query.filter_by(email=email).first()
    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404