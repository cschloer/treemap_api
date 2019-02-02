from flask import Blueprint, request, jsonify
import base64
import secrets
import hashlib
from ..exceptions import FormError, InvalidUsage


crypto_bp = Blueprint("crypto", __name__)

@crypto_bp.route('/', methods=['GET'])
def crypto():
    if request.method == 'GET':
        verifier = base64.b64encode(secrets.token_bytes(32))
        verifier = verifier.replace(b'+', b'-').replace(b'/', b'_').replace(b'=', b'')

        hasher = hashlib.sha256()
        hasher.update(verifier)
        challenge = base64.b64encode(hasher.digest())
        challenge = challenge.replace(b'+', b'-').replace(b'/', b'_').replace(b'=', b'')
        return jsonify({
            'verifier': verifier.decode('utf-8'),
            'challenge': challenge.decode('utf-8'),
        })
