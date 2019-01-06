from ..database import db
from datetime import datetime

class TreeSpeciesVote(db.Model):
    __tablename__ = 'treespeciesvote'
    id = db.Column('tree_species_vote_id', db.Integer, primary_key=True)
    user_id = db.Column(db.String(60), nullable=False)
    tree_id = db.Column(db.Integer, db.ForeignKey('tree.tree_id'), nullable=False)
    species_id = db.Column(
        db.Integer,
        db.ForeignKey('species.species_id'),
        nullable=False,
    )
    created = db.Column(db.DateTime)
    species = db.relationship('Species')

    def __init__(self, user_id, tree_id, species_id):
        self.user_id = user_id
        self.species_id = species_id
        self.tree_id = tree_id
        self.created = datetime.utcnow()

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'species_id': self.species_id,
            'tree_id': self.tree_id,
            'created': self.created,
            'species': self.species.to_dict(),
        }
