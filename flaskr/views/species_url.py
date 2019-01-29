from flask import Blueprint, request, jsonify
from ..models import SpeciesUrl
from ..exceptions import FormError, InvalidUsage
from .base import index, create, get, update, delete
from ..decorators import add_user_names

species_url_bp = Blueprint("speciesurl", __name__)

@species_url_bp.route('/', methods=('GET', 'POST'))
def species_url():
    if request.method == 'GET':
        return index(SpeciesUrl, request.args.copy())
    if request.method == 'POST':
        return create(SpeciesUrl, request.json)

@species_url_bp.route('/<int:id_>', methods=[])
def species_url_id(id_):
    if request.method == 'DELETE':
        return delete(SpeciesUrl, id_)

