from flask import Blueprint, request, jsonify
from ..models import Tree, TreeLocation, TreeLocationVote, TreeSpeciesVote
from ..exceptions import FormError, InvalidUsage
from .base import index, create, get, update, delete
from ..database import db


tree_bp = Blueprint("tree", __name__)

@tree_bp.route('/', methods=('GET', 'POST'))
def tree():
    if request.method == 'GET':
        return index(Tree, request.args.to_dict())
    if request.method == 'POST':
        # A custom POST to allow all of the objects to be added at the same time
        locations = request.json.pop('locations', None)
        species_votes = request.json.pop('species_votes', None)
        tree = create(Tree, request.json, False, False)
        tree_id = tree['id']

        if not locations:
            raise FormError(f'A tree must have a location')
        location_dicts = []
        for location_request in locations:
            votes = location_request.pop('votes', None)
            location_request['tree_id'] = tree_id
            location = create(TreeLocation, location_request, False, False)
            location_id = location['id']
            vote_dicts = []
            if votes:
                for vote_request in votes:
                    vote_request['tree_location_id'] = location_id
                    vote = create(TreeLocationVote, vote_request, False, False)
                    vote_dicts.append(vote)
            location['votes'] = vote_dicts
            location_dicts.append(location)
        tree['locations'] = location_dicts

        vote_dicts = []
        if species_votes:
            for vote_request in species_votes:
                vote_request['tree_id'] = tree_id
                vote = create(TreeSpeciesVote, vote_request, False, False)
                vote_dicts.append(vote)
        tree['species_votes'] = vote_dicts


        db.session.commit()

        return jsonify(tree)


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

