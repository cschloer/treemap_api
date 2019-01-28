from flask import g
import time
import requests
from .redis import redis

def get_auth0_access_token():
    expires_at = redis.get('auth0_access_token_expires_at')
    if not expires_at:
        expires_at = 0
    else:
        expires_at = int(expires_at)
    expired = expires_at - time.time() < 0

    if expired or not redis.exists('auth0_access_token'):
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
        redis.set('auth0_access_token_expires_at', expires_at)
        redis.set('auth0_access_token', token['access_token'])

    access_token = redis.get('auth0_access_token')
    return access_token

def get_user_names(user_ids):
    ''' A function that takes in a list of user_ids and returns a dictionary connecting user_id to user_name '''
    user_names = {}
    unknown_user_ids = []
    for user_id in user_ids:
        user_name = redis.get(user_id)
        if user_name:
            user_names[user_id] = user_name
        else:
            unknown_user_ids.append(user_id)

    if len(unknown_user_ids):
        access_token = get_auth0_access_token()
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
                first_name = user['given_name']
                last_initial = f' {user["family_name"][0]}.' if user['family_name'] else ''
                user_name = f'{first_name}{last_initial}'
                # Add the username to the return object
                user_names[user['user_id']] = user_name
                # Add the username to the cache
                redis.set(user['user_id'], user_name)
        else:
            print(f'ERROR when making request to auth0: {res.status_code}')

    for user_id in unknown_user_ids:
        # Find all user ids that were not found
        if user_id not in user_names:
            user_names[user_id] = 'Unknown user'
            redis.set(user_id, 'Unknown user')

    return user_names
