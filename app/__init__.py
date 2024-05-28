from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import secrets
import csv
from pathlib import Path
import os

# Initialize SQLAlchemy and Marshmallow
db = SQLAlchemy()
ma = Marshmallow()

def create_app(test_config=None):
    # Create a Flask instance
    app = Flask(__name__, instance_relative_config=True)
    
    # Basic configuration of the application
    app.config.from_mapping(
        SECRET_KEY='Jvo09P5Wxf3WF-xSyJNlUQ',  # Important for session management and signing
        SQLALCHEMY_DATABASE_URI='sqlite:///mydatabase.db',  # Database file location
        SQLALCHEMY_TRACK_MODIFICATIONS=False  # To avoid overhead
    )

    # Load configuration from 'config.py' if not in test mode
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Initialize extensions with the app instance
    db.init_app(app)
    ma.init_app(app)

    # Importing models here to avoid circular imports
    from .models import User, Request

    # Simple route as a sanity check
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # Create database tables and populate data if not already done
    with app.app_context():
        db.create_all()
        add_data_from_csv()

        # Register blueprints
        from app import routes
        app.register_blueprint(routes.bp)
    return app

def add_data_from_csv():
    # Load initial data from CSV into the database
    from .models import Request
   
    # Only add data if no data is currently present
    if not Request.query.first():
        print("Adding initial request data to the database.")
        request_file = Path(__file__).parent.parent.joinpath("data", "dataset_prepared.csv")
        with open(request_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header row
            for row in csv_reader:
                request = Request(
                    case_type=row[0],
                    status=row[1],
                    request_received_year=row[2] if row[2] else None,
                    request_received_quarter=row[3] if row[3] else None,
                    request_received_month=row[4],
                    case_active_days_grouped=row[5]
                )
                db.session.add(request)
            db.session.commit()
        print("Data added successfully.")
