from flask import Blueprint, request, jsonify
from ..models.user import User
from .base import index, create, get, update


user_bp = Blueprint("user", __name__)

@user_bp.route('/', methods=('GET', 'POST'))
def user():
    if request.method == 'GET':
        return index(User, request.args.to_dict())
    if request.method == 'POST':
        return create(User, request.json)

@user_bp.route('/<int:id_>', methods=('GET', 'PUT'))
def user_id(id_):
    if request.method == 'GET':
        return get(User, id_)
    if request.method == 'PUT':
        return update(User, request.json, id_)

