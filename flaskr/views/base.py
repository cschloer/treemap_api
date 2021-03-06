from flask import jsonify
from ..exceptions import InvalidUsage, FormError
from ..database import db

def index(model, filter_args):
    ''' A base index function '''
    query = model.query

    order = filter_args.pop('order', 'desc')
    if order == 'asc':
        query = query.order_by(model.created.asc())
    elif order == 'desc':
        query = query.order_by(model.created.desc())
    else:
        raise InvalidUsage('order filter param must be one of \'desc\' or \'asc\'')

    limit = filter_args.pop('limit', None)

    query = query.filter_by(**filter_args)

    if limit:
        try:
            limit = int(limit)
        except ValueError:
            raise InvalidUsage(
                f'limit filter param must be an integer. Unable to convert \'{limit}\' to an integer'
            )
        query = query.limit(limit)

    return jsonify([
        m.to_dict() for m
        in query.all()
    ])

def create(model, form):
    ''' A base create function '''
    try:
        m = model(**form)
    except KeyError as e:
        raise FormError(f'Missing a value in the form: {str(e)}')
    db.session.add(m)
    db.session.commit()
    return jsonify(m.to_dict())

def get(model, id_):
    ''' A base get by id function '''
    return jsonify(model.query.get(id_).to_dict())

def update(model, form, id_):
    ''' A base update function '''
    model.query.filter_by(id=id_).update(form)
    m = model.query.get(id_).to_dict()
    db.session.commit()
    return jsonify(m)
