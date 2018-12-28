from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .models import *
from .database import db
from .exceptions import InvalidUsage, FormError
from .views import user_plant_bp, user_plant_image_bp
import os


app = Flask(__name__)

gstones = 0

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
    GOOGLE_CLOUD_PROJECT_ID=os.environ['GOOGLE_CLOUD_PROJECT_ID'],
    GOOGLE_CLOUD_STORAGE_BUCKET=os.environ['GOOGLE_CLOUD_STORAGE_BUCKET'],
    GOOGLE_CLOUD_ALLOWED_EXTENSIONS=os.environ['GOOGLE_CLOUD_ALLOWED_EXTENSIONS'].split(','),
)

app.register_blueprint(user_plant_bp, url_prefix='/userplant')
app.register_blueprint(user_plant_image_bp, url_prefix='/userplantimage')

with app.app_context():
    db.init_app(app)
    db.create_all()
migrate = Migrate(app, db)
