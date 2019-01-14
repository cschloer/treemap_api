from flask import Blueprint, request, jsonify
from ..models import Post
from ..exceptions import FormError, InvalidUsage
from .base import index, create, get, update, delete


post_bp = Blueprint("post", __name__)

@post_bp.route('/', methods=('GET', 'POST'))
def post():
    if request.method == 'GET':
        return index(Post, request.args.to_dict())
    if request.method == 'POST':
        return create(Post, request.json)

@post_bp.route('/<int:id_>', methods=())
def post_id(id_):
    if request.method == 'DELETE':
        return delete(Post, id_)

