from flask import Blueprint, request, jsonify, current_app
from google.cloud import storage
from werkzeug import secure_filename
import datetime
import io
import six
import base64

from ..models import TreeImage
from .base import index, create, get, update, delete
from ..exceptions import InvalidUsage
from ..decorators import basic_authorization


tree_image_bp = Blueprint("treeimage", __name__)

@tree_image_bp.route('/', methods=('GET', 'POST'))
@basic_authorization
def tree_image():
    if request.method == 'GET':
        return index(TreeImage, request.args.copy())
    if request.method == 'POST':
        return create(TreeImage, request.json)

@tree_image_bp.route('/<int:id_>', methods=('GET', 'PUT', 'DELETE'))
@basic_authorization
def tree_image_id(id_):
    if request.method == 'GET':
        return get(TreeImage, id_)
    if request.method == 'PUT':
        return update(TreeImage, request.json, id_)
    if request.method == 'DELETE':
        return delete(TreeImage, id_)

@tree_image_bp.route('/storage/', methods=('POST',))
@basic_authorization
def tree_image_storage():
    if request.method == 'POST':
        args = request.json
        base64_data = args.get('base64')
        data = base64.decodebytes(base64_data.encode())
        url = upload_file(data, args.get('name'), args.get('content_type'))
        return jsonify({'url': url})


def _get_storage_client():
    return storage.Client(
        project=current_app.config['GOOGLE_CLOUD_PROJECT_ID']
    )

def _check_extension(filename, allowed_extensions):
    if (
        '.' not in filename
        or filename.split('.').pop().lower() not in allowed_extensions
    ):
        raise InvalidUsage(
            "{0} has an invalid name or extension".format(filename)
        )


def _safe_filename(filename):
    """
    Generates a safe filename that is unlikely to collide with existing objects
    in Google Cloud Storage.
    ``filename.ext`` is transformed into ``filename-YYYY-MM-DD-HHMMSS.ext``
    """
    filename = secure_filename(filename)
    date = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
    basename, extension = filename.rsplit('.', 1)
    return "{0}-{1}.{2}".format(basename, date, extension)

def upload_file(file_stream, filename, content_type):
    """
    Uploads a file to a given Cloud Storage bucket and returns the public url
    to the new object.
    """
    _check_extension(filename, current_app.config['GOOGLE_CLOUD_ALLOWED_EXTENSIONS'])
    filename = _safe_filename(filename)

    client = _get_storage_client()
    bucket = client.bucket(current_app.config['GOOGLE_CLOUD_STORAGE_BUCKET'])
    blob = bucket.blob(filename)

    blob.upload_from_string(
        file_stream,
        content_type=content_type
    )

    url = blob.public_url

    if isinstance(url, six.binary_type):
        url = url.decode('utf-8')

    return url
