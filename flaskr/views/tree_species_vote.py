from flask import Blueprint, request, jsonify
from ..models import TreeSpeciesVote
from ..exceptions import FormError, InvalidUsage
from .base import index, create, get, update, delete


tree_species_vote_bp = Blueprint("tree_species_vote", __name__)

@tree_species_vote_bp.route('/', methods=('GET', 'POST'))
def tree_species_vote():
    if request.method == 'GET':
        return index(TreeSpeciesVote, request.args.copy())
    if request.method == 'POST':
        return create(TreeSpeciesVote, request.json)

@tree_species_vote_bp.route('/<int:id_>', methods=('GET', 'PUT', 'DELETE'))
def tree_species_vote_id(id_):
    if request.method == 'GET':
        return get(TreeSpeciesVote, id_)
    if request.method == 'PUT':
        if request.json.get('user_id'):
            raise FormError(f'The user_id of a tree_species_vote object ({id_}) cannot be changed')
        return update(TreeSpeciesVote, request.json, id_)
    if request.method == 'DELETE':
        return delete(TreeSpeciesVote, id_)

