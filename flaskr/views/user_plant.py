from flask import Blueprint, request, jsonify
from ..models import UserPlant
from ..exceptions import FormError
from .base import index, create, get, update, delete


user_plant_bp = Blueprint("userplant", __name__)

@user_plant_bp.route('/', methods=('GET', 'POST'))
def user_plant():
    if request.method == 'GET':
        return index(UserPlant, request.args.to_dict())
    if request.method == 'POST':
        return create(UserPlant, request.json)

@user_plant_bp.route('/<int:id_>', methods=('GET', 'PUT', 'DELETE'))
def user_plant_id(id_):
    if request.method == 'GET':
        return get(UserPlant, id_)
    if request.method == 'PUT':
        if request.json.get('user_id'):
            raise FormError(f'The user_id of a user_plant object ({id_}) cannot be changed')
        return update(UserPlant, request.json, id_)
    if request.method == 'DELETE':
        return delete(UserPlant, id_)

