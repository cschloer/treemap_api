from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from .models.user import User
from .database import db
from .exceptions import InvalidUsage, FormError
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

@app.route('/user', methods=['GET', 'POST', 'PUT'])
def user():
    if request.method == 'GET':
        return jsonify([
            user.to_dict() for user
            in User.query.order_by(User.created.desc()).all()
        ])

    elif request.method == 'POST':
        try:
            form = request.json
            user = User(
                form['auth0_id'],
                form['name'],
            )
        except KeyError as e:
            raise e
            raise FormError(f'Missing a value in the form: {str(e)}')
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict())

    elif request.method == 'PUT':
        pass
    raise InvalidUsage('Yooo invalid')


@app.route('/update', methods=['POST'])
def update_done():
    for todo in User.query.all():
        todo.done = ('done.%d' % todo.id) in request.form
    flash('Updated status')
    db.session.commit()
    return redirect(url_for('show_all'))
