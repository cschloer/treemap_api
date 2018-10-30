from ..database import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column('user_id', db.Integer, primary_key=True)
    auth0_id = db.Column(db.String(60))
    name = db.Column(db.String)
    created = db.Column(db.DateTime)

    def __init__(self, auth0_id, name):
        self.auth0_id = auth0_id
        self.name = name
        self.created = datetime.utcnow()

    def to_dict(self):
        return {
            'id': self.id,
            'auth0_id': self.auth0_id,
            'name': self.name,
            'created': self.created,
        }
