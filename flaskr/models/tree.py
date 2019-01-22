from ..database import db
from datetime import datetime
from ..helpers import transform_species_votes

class Tree(db.Model):
    __tablename__ = 'tree'
    id = db.Column('tree_id', db.Integer, primary_key=True)
    user_id = db.Column(db.String(60), nullable=False)
    latitude = db.Column(db.Float(12))
    longitude = db.Column(db.Float(12))
    species_votes = db.relationship('TreeSpeciesVote', lazy='joined')
    images = db.relationship('TreeImage', lazy='joined')
    created = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', back_populates='tree', lazy='noload')

    def __init__(self, user_id, latitude, longitude):
        self.user_id = user_id
        self.latitude = latitude
        self.longitude = longitude

    def to_dict(self):
        # Tally the votes in a dictionary
        species_votes = transform_species_votes(self.species_votes)

        images = [image.to_dict() for image in self.images]
        return {
            'id': self.id,
            'user_id': self.user_id,
            'created': self.created,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'species_votes': species_votes,
            'images': images,
        }
