from app import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}  # Add this line

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    email: Mapped[str] = mapped_column(db.Text, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.Text, unique=True, nullable=False)

class Request(db.Model):
    __tablename__ = 'request'
    __table_args__ = {'extend_existing': True}  # Add this line
    __mapper_args__ = {
        'confirm_deleted_rows': False
    }
    
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    case_type: Mapped[str] = mapped_column(db.String(128), nullable=False, index=True)
    status: Mapped[str] = mapped_column(db.String(128), nullable=False, index=True)
    request_received_year: Mapped[int] = mapped_column(db.String(128), nullable=False, index=True)
    request_received_quarter: Mapped[str] = mapped_column(db.String(128), nullable=False, index=True)
    request_received_month: Mapped[str] = mapped_column(db.String(128))
    case_active_days_grouped: Mapped[str] = mapped_column(db.String(128))