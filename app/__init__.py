from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_marshmallow import Marshmallow
import secrets
import csv
from pathlib import Path
import os

# could cause problems of model_class is not DeclarativeBase
db = SQLAlchemy()
ma = Marshmallow()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    # Configuring the app
    app.config.from_mapping(
        SECRET_KEY='Jvo09P5Wxf3WF-xSyJNlUQ',
        SQLALCHEMY_DATABASE_URI='sqlite:///mydatabase.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Initialise Flask with the SQLAlchemy database extension
    db.init_app(app)
    ma.init_app(app)

    from .models import User, Request

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    with app.app_context():
        # routes.setup_routes(app)
        db.create_all()
        add_data_from_csv()

        from app import routes
        app.register_blueprint(routes.bp)
    return app

def add_data_from_csv():
    from .models import Request
   
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