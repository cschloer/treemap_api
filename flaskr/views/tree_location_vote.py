from flask import Blueprint, request, jsonify
from ..models import TreeLocationVote
from ..exceptions import FormError, InvalidUsage
from .base import index, create, get, update, delete


tree_location_vote_bp = Blueprint("tree_location_vote", __name__)

@tree_location_vote_bp.route('/', methods=('GET', 'POST'))
def tree_location_vote():
    if request.method == 'GET':
        return index(TreeLocationVote, request.args.to_dict())
    if request.method == 'POST':
        return create(TreeLocationVote, request.json)

@tree_location_vote_bp.route('/<int:id_>', methods=('GET', 'PUT', 'DELETE'))
def tree_location_vote_id(id_):
    if request.method == 'GET':
        return get(TreeLocationVote, id_)
    if request.method == 'PUT':
        if request.json.get('user_id'):
            raise FormError(f'The user_id of a tree_location_vote object ({id_}) cannot be changed')
        return update(TreeLocationVote, request.json, id_)
    if request.method == 'DELETE':
        return delete(TreeLocationVote, id_)

