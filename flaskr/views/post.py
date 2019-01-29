from flask import Blueprint, request, jsonify
from ..models import Post
from ..exceptions import FormError, InvalidUsage
from .base import index, create, get, update, delete
from .tree import create_tree
from ..database import db
from ..decorators import add_user_names


post_bp = Blueprint("post", __name__)

@post_bp.route('/', methods=('GET', 'POST'))
@add_user_names
def post():
    if request.method == 'GET':
        return index(Post, request.args.copy())
    if request.method == 'POST':
        # Handle creating a tree first if the tree has not been created
        if not request.json.get('tree_id', None):
            tree_form = request.json.pop('tree', None)
            if tree_form:
                tree = create_tree(tree_form)
                request.json['tree_id'] = tree['id']
            else:
                raise FormError(f'If tree_id is not passed to a Post post request, a tree form must be added')
        post = create(Post, request.json, False, False)

        db.session.commit()
        return jsonify(post)

@post_bp.route('/<int:id_>', methods=('GET',))
@add_user_names
def post_id(id_):
    if request.method == 'GET':
        return get(Post, id_)
    if request.method == 'DELETE':
        return delete(Post, id_)

