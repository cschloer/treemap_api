from flask import Flask, request, _request_ctx_stack
from six.moves.urllib.request import urlopen
from flask_cors import cross_origin
from .exceptions import AuthError, ServerError
from jose import jwt
import json
import os
import time
import requests
from .redis import redis
from .shelf import get_shelf
from .settings import Settings

def get_auth0_access_token(shelf):
    expires_at = 0
    if 'auth0_access_token_expires_at' in shelf:
        expires_at = shelf['expires_at']
    expired = expires_at - time.time() < 0

    if expired or not 'auth0_access_token' in shelf:
        res = requests.post(
            'https://treemap.auth0.com/oauth/token',
            data={

                'grant_type': 'client_credentials',
                'client_id': 'jpoLN1eNKub3Yg8KNwrc5UZqlbou4LFX',
                'client_secret': 'URschkUqUrfxvr0qwREVyzd6y6qhZd7OmqhSyB_xrqt6iEqwJ3IfhQ3l1FhGbuYf',
                'audience': 'https://treemap.auth0.com/api/v2/'
            },
        )
        token = res.json()
        expires_at = token['expires_in'] + int(time.time()) - 10
        shelf['auth0_access_token_expires_at'] = expires_at
        shelf['auth0_access_token'] = token['access_token']

    access_token = shelf['auth0_access_token']
    return access_token

def get_user_names(user_ids):
    ''' A function that takes in a list of user_ids and returns a dictionary connecting user_id to user_name '''
    user_names = {}
    unknown_user_ids = []
    with get_shelf() as shelf:
        for user_id in user_ids:
            user_name = shelf.get(user_id)
            if user_name:
                user_names[user_id] = user_name
            else:
                unknown_user_ids.append(user_id)

        if len(unknown_user_ids):
            access_token = get_auth0_access_token(shelf)
            params = {
                'q': ' OR '.join([f'user_id:{user_id}' for user_id in unknown_user_ids]),
                'search_engine': 'v3',
            }
            res = requests.get(
                f'https://treemap.auth0.com/api/v2/users',
                headers={
                    'authorization': f'Bearer {access_token}'
                },
                params=params,

            )
            if res.status_code == 200:
                users = res.json()
                # Iterate through all of the newfound users
                for user in users:
                    user_name = 'user'
                    if 'given_name' in user:
                        first_name = user['given_name']
                        last_initial = f' {user["family_name"][0]}.' if user['family_name'] else ''
                        user_name = f'{first_name}{last_initial}'
                    elif 'nickname' in user:
                        user_name = user['nickname']
                    elif 'name' in user:
                        user_name = user['name']
                    # Add the username to the return object
                    user_names[user['user_id']] = user_name
                    # Add the username to the cache
                    shelf[user['user_id']] = user_name
            else:
                print(f'ERROR when making request to auth0: {res.status_code}')

        for user_id in unknown_user_ids:
            # Find all user ids that were not found
            if user_id not in user_names:
                user_names[user_id] = 'Unknown user'
                shelf[user_id] = 'Unknown user'

        return user_names

def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError('Authorization header is expected')

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError('Authorization header must start with "Bearer"')
    elif len(parts) == 1:
        raise AuthError('Token not found')
    elif len(parts) > 2:
        raise AuthError('Authorization header must be "Bearer token"')

    token = parts[1]
    return token

def verify_auth():
    AUTH0_DOMAIN = Settings.get('AUTH0_DOMAIN')
    AUTH0_API_AUDIENCE = Settings.get('AUTH0_API_AUDIENCE')
    AUTH0_ALGORITHMS_STRING = Settings.get('AUTH0_ALGORITHMS')
    if not AUTH0_DOMAIN or not AUTH0_API_AUDIENCE or not AUTH0_ALGORITHMS_STRING:
        raise ServerError('One or more AUTH0 environment variables not set')
    AUTH0_ALGORITHMS = AUTH0_ALGORITHMS_STRING.split(',')


    token = get_token_auth_header()
    jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=AUTH0_ALGORITHMS,
                audience=AUTH0_API_AUDIENCE,
                issuer=f'https://{AUTH0_DOMAIN}/',
            )
        except jwt.ExpiredSignatureError:
            print('Token expired')
            raise AuthError('Token is expired')
        except jwt.JWTClaimsError as e:
            print('Incorect claims')
            raise e
            raise AuthError('Incorrect claims, please check the audience and issuer')
        except Exception as e:
            print('unable to parse authentictn')
            raise e
            raise AuthError('Unable to parse authentication')

        _request_ctx_stack.top.current_user = payload
        return True
    print('Invalid header')
    raise AuthError('Invalid header, unable to find appropriate key')

