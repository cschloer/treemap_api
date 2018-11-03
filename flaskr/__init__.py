from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .models.user import User
from .database import db
from .exceptions import InvalidUsage, FormError
from .views import user
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

db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(user, url_prefix='/user')
