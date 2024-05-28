import jwt
from datetime import datetime, timedelta, timezone
from flask import make_response, request, jsonify, current_app as app
from functools import wraps
from app import db
from app.models import User
import re

def encode_auth_token(user_id):
    """Generates an authentication token with a short expiration for user identification."""
    try:
        # Set token to expire in 30 seconds for security and testing purposes
        payload = {
            'exp': datetime.now(timezone.utc) + timedelta(seconds=30),
            'iat': datetime.now(timezone.utc),
            'sub': user_id
        }
        # Encode the payload using the application's secret key and the HS256 algorithm
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),  # Retrieve the secret key from app config
            algorithm='HS256'
        )
    except Exception as e:
        return e  # Return the exception if encoding fails

def decode_auth_token(auth_token):
    """
    Decodes the auth token and validates it against the secret key.
    Returns the payload if the token is valid or a response if it fails validation.
    """
    try:
        payload = jwt.decode(auth_token, app.config.get("SECRET_KEY"), algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return make_response({'message': "Token expired. Please log in again."}, 401)
    except jwt.InvalidTokenError:
        return make_response({'message': "Invalid token. Please log in again."}, 401)
    

def token_required(f):
    """Decorator to ensure that a valid token is passed with HTTP requests."""
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization', None)
        if not token:
            return jsonify({'message': 'Authentication Token missing'}), 401
        
        try:
            # Check if the token is properly formatted
            if token.startswith('Bearer '):
                token = token[7:]  # Strip "Bearer " prefix to isolate the token itself
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = decoded_token['sub']
            current_user = db.session.execute(
                db.select(User).filter_by(id=current_user_id)
            ).scalar_one_or_none()

            if not current_user:
                return jsonify({'message': 'Invalid or missing token.'}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except (jwt.InvalidTokenError, Exception) as e:
            return jsonify({'message': 'Invalid token', 'error': str(e)}), 401

        return f(*args, **kwargs)

    return decorator

def is_valid_email(email):
    """Check if the provided email address matches the expected format."""
    email_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return re.match(email_regex, email, re.IGNORECASE)

def requires_role(required_role):
    """Decorator to enforce role-based access control (RBAC) for routes."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_token = request.headers.get('Authorization').split(" ")[1]
            data = jwt.decode(auth_token, app.config['SECRET_KEY'], algorithms=["HS256"])
            user = User.query.filter_by(id=data['sub']).first()
            if not user or user.role != required_role:
                return jsonify({'message': 'Unauthorized. Insufficient permissions'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator
