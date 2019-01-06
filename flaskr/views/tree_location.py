from flask import Blueprint, request, jsonify
from ..models import TreeLocation
from ..exceptions import FormError, InvalidUsage
from .base import index, create, get, update, delete


tree_location_bp = Blueprint("tree_location", __name__)

@tree_location_bp.route('/', methods=('GET', 'POST'))
def tree_location():
    if request.method == 'GET':
        return index(TreeLocation, request.args.to_dict())
    if request.method == 'POST':
        return create(TreeLocation, request.json)

@tree_location_bp.route('/<int:id_>', methods=('GET', 'PUT', 'DELETE'))
def tree_location_id(id_):
    if request.method == 'GET':
        return get(TreeLocation, id_)
    if request.method == 'PUT':
        if request.json.get('user_id'):
            raise FormError(f'The user_id of a tree_location object ({id_}) cannot be changed')
        return update(TreeLocation, request.json, id_)
    if request.method == 'DELETE':
        return delete(TreeLocation, id_)

