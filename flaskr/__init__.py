from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .models import *
from .database import db
from .redis import redis
from .exceptions import (
    InvalidUsage, FormError,
    AuthError, ServerError,
)
from .views import (
    tree_bp, species_bp, tree_species_vote_bp,
    tree_image_bp, post_bp, post_comment_bp,
    species_url_bp, crypto_bp,
)
import os


app = Flask(__name__)

@app.errorhandler(InvalidUsage)
@app.errorhandler(FormError)
@app.errorhandler(AuthError)
@app.errorhandler(ServerError)
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

app.register_blueprint(tree_bp, url_prefix='/tree')
app.register_blueprint(species_bp, url_prefix='/species')
app.register_blueprint(species_url_bp, url_prefix='/speciesurl')
app.register_blueprint(tree_species_vote_bp, url_prefix='/treespeciesvote')
app.register_blueprint(tree_image_bp, url_prefix='/treeimage')
app.register_blueprint(post_bp, url_prefix='/post')
app.register_blueprint(post_comment_bp, url_prefix='/postcomment')
app.register_blueprint(crypto_bp, url_prefix='/crypto')

with app.app_context():
    db.init_app(app)
    db.create_all()
migrate = Migrate(app, db)
