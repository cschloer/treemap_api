from flask import current_app
import os
import shelve

# A file-like cache to replace redis
# because redis cannot be used in the google-cloud free tier (lol)
path = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..',
        'cache',
    )
)
fname = os.path.join(path, 'cachefile')

def get_shelf():
    print('returning open shelf')
    return shelve.open(fname)

#def get_value(key):
#    with shelve.open(fname) as shelf:
#        return shelf[key]
