from functools import wraps
from .helpers import add_usernames
import json

def add_user_names(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        res =  f(*args, **kwargs)
        data = res.get_json()
        if type(data) is dict or type(data) is list:
            data = add_usernames(data)
            res.set_data(json.dumps(data))
        return res
    return decorated_function
