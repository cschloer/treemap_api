from flask import Blueprint, request, jsonify
from ..models import Tree
from ..exceptions import FormError, InvalidUsage
from .base import index, create, get, update, delete


tree_bp = Blueprint("tree", __name__)

@tree_bp.route('/', methods=('GET', 'POST'))
def tree():
    if request.method == 'GET':
        return index(Tree, request.args.to_dict())
    if request.method == 'POST':
        return create(Tree, request.json)

@tree_bp.route('/<int:id_>', methods=('GET', 'PUT', 'DELETE'))
def tree_id(id_):
    if request.method == 'GET':
        return get(Tree, id_)
    if request.method == 'PUT':
        if request.json.get('user_id'):
            raise FormError(f'The user_id of a tree object ({id_}) cannot be changed')
        return update(Tree, request.json, id_)
    if request.method == 'DELETE':
        return delete(Tree, id_)

