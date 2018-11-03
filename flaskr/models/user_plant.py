from ..database import db
from datetime import datetime

class UserPlant(db.Model):
    __tablename__ = 'user_plant'
    id = db.Column('user_plant_id', db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    name = db.Column(db.String)
    created = db.Column(db.DateTime)

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.created = datetime.utcnow()

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'created': self.created,
        }
