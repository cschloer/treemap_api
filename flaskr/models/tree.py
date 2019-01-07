from ..database import db
from datetime import datetime

class Tree(db.Model):
    __tablename__ = 'tree'
    id = db.Column('tree_id', db.Integer, primary_key=True)
    user_id = db.Column(db.String(60), nullable=False)
    created = db.Column(db.DateTime)
    latitude = db.Column(db.Float(12))
    longitude = db.Column(db.Float(12))
    species_votes = db.relationship('TreeSpeciesVote', lazy="joined")

    def __init__(self, user_id, latitude, longitude):
        self.user_id = user_id
        self.latitude = latitude
        self.longitude = longitude
        self.created = datetime.utcnow()

    def to_dict(self):
        species_votes = [species_vote.to_dict() for species_vote in self.species_votes]
        return {
            'id': self.id,
            'user_id': self.user_id,
            'created': self.created,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'species_votes': species_votes,
        }
