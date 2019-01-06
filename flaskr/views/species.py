from flask import Blueprint, request, jsonify
from ..models import Species
from ..exceptions import FormError, InvalidUsage
from .base import index, create, get, update, delete


species_bp = Blueprint("species", __name__)

@species_bp.route('/', methods=('GET', 'POST'))
def species():
    if request.method == 'GET':
        return index(Species, request.args.to_dict())
    if request.method == 'POST':
        return create(Species, request.json)

@species_bp.route('/<int:id_>', methods=())
def species_id(id_):
    if request.method == 'DELETE':
        return delete(Species, id_)

