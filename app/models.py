from app import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class User(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    email: Mapped[str] = mapped_column(db.Text, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.Text, unique=True, nullable=False)

class Dataset(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    case_type: Mapped[str] = mapped_column(db.String(128), nullable=False, index=True)
    status: Mapped[str] = mapped_column(db.String(128), nullable=False, index=True)
    request_received_year: Mapped[int] = mapped_column(db.String(128), nullable=False, index=True)
    request_received_quarter: Mapped[str] = mapped_column(db.String(128), nullable=False, index=True)
    request_received_month: Mapped[str] = mapped_column(db.String(128))
    case_active_days_grouped: Mapped[str] = mapped_column(db.String(128))