from ..database import db
from datetime import datetime

class Tree(db.Model):
    __tablename__ = 'tree'
    id = db.Column('tree_id', db.Integer, primary_key=True)
    user_id = db.Column(db.String(60), nullable=False)
    created = db.Column(db.DateTime)
    locations = db.relationship('TreeLocation', lazy="joined")
    species_votes = db.relationship('TreeSpeciesVote', lazy="joined")

    def __init__(self, user_id):
        self.user_id = user_id
        self.created = datetime.utcnow()

    def to_dict(self):
        locations = [location.to_dict() for location in self.locations]
        species_votes = [species_vote.to_dict() for species_vote in self.species_votes]
        return {
            'id': self.id,
            'user_id': self.user_id,
            'created': self.created,
            'locations': locations,
            'species_votes': species_votes,
        }
