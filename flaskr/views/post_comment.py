from flask import Blueprint, request, jsonify
from ..models import PostComment
from ..exceptions import FormError, InvalidUsage
from .base import index, create, get, update, delete


post_comment_bp = Blueprint("postcomment", __name__)

@post_comment_bp.route('/', methods=('GET', 'POST'))
def post_comment():
    if request.method == 'GET':
        return index(PostComment, request.args.to_dict())
    if request.method == 'POST':
        return create(PostComment, request.json)

@post_comment_bp.route('/<int:id_>', methods=())
def post_comment_id(id_):
    if request.method == 'DELETE':
        return delete(PostComment, id_)

