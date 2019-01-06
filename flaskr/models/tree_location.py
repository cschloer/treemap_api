from ..database import db
from datetime import datetime

class TreeLocation(db.Model):
    __tablename__ = 'treelocation'
    id = db.Column('tree_location_id', db.Integer, primary_key=True)
    user_id = db.Column(db.String(60), nullable=False)
    tree_id = db.Column(db.Integer, db.ForeignKey('tree.tree_id'), nullable=False)
    latitude = db.Column(db.Float(12))
    longitude = db.Column(db.Float)
    created = db.Column(db.DateTime)
    votes = db.relationship('TreeLocationVote')

    def __init__(self, user_id, tree_id, latitude, longitude):
        self.user_id = user_id
        self.tree_id = tree_id
        self.latitude = latitude
        self.longitude = longitude
        self.created = datetime.utcnow()

    def to_dict(self):
        print('lat', self.latitude)
        print('user_id', self.user_id)
        return {
            'id': self.id,
            'user_id': self.user_id,
            'tree_id': self.tree_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'created': self.created,
            'votes': [vote.to_dict() for vote in self.votes],
        }
