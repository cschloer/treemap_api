from ..database import db
from datetime import datetime

class TreeLocationVote(db.Model):
    __tablename__ = 'treelocationvote'
    id = db.Column('tree_location_vote_id', db.Integer, primary_key=True)
    user_id = db.Column(db.String(60), nullable=False)
    tree_location_id = db.Column(
        db.Integer,
        db.ForeignKey('treelocation.tree_location_id'),
        nullable=False,
    )
    created = db.Column(db.DateTime)

    def __init__(self, user_id, tree_location_id):
        self.user_id = user_id
        self.tree_location_id = tree_location_id
        self.created = datetime.utcnow()

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'tree_location_id': self.tree_location_id,
            'created': self.created,
        }
