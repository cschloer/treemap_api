from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .models import *
from .database import db
from .exceptions import InvalidUsage, FormError
from .views import user_plant_bp
import os


app = Flask(__name__)

@app.errorhandler(InvalidUsage)
@app.errorhandler(FormError)
def handle_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

app.config.from_mapping(
    SECRET_KEY='dev',
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'flaskr.sqlite'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

app.register_blueprint(user_plant_bp, url_prefix='/userplant')

with app.app_context():
    db.init_app(app)
    db.create_all()
migrate = Migrate(app, db)
