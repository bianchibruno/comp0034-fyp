from app import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    # Define the tablename for SQLAlchemy.
    __tablename__ = 'user'
    # This allows the model to extend or replace a table that already exists without an error.
    __table_args__ = {'extend_existing': True}

    # User attributes with data types and constraints
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    # New attribute 'role' with default value 'user' for role-based access control
    role = db.Column(db.String(10), default='user')

    @property
    def password(self):
        # Prevent reading the password directly
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        # Store password as a hash for security
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        # Verify the hash against the input password
        return check_password_hash(self.password_hash, password)

class Request(db.Model):
    # Define the tablename for SQLAlchemy.
    __tablename__ = 'request'
    # This allows the model to extend or replace a table that already exists without an error.
    __table_args__ = {'extend_existing': True}
    # Configure SQLAlchemy to not confirm row deletions (helpful for bulk operations or special contexts).
    __mapper_args__ = {
        'confirm_deleted_rows': False
    }
    
    # Define mapped columns for the request data with types, indexes, and nullability
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    case_type: Mapped[str] = mapped_column(db.String(128), nullable=False, index=True)
    status: Mapped[str] = mapped_column(db.String(128), nullable=False, index=True)
    request_received_year: Mapped[int] = mapped_column(db.String(128), nullable=False, index=True)
    request_received_quarter: Mapped[str] = mapped_column(db.String(128), nullable=False, index=True)
    request_received_month: Mapped[str] = mapped_column(db.String(128))
    case_active_days_grouped: Mapped[str] = mapped_column(db.String(128))
