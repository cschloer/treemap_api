from ..database import db
from datetime import datetime

class TreeImage(db.Model):
    __tablename__ = 'treeimage'
    id = db.Column('tree_image_id', db.Integer, primary_key=True)
    user_id = db.Column(db.String(60), nullable=False)
    tree_id = db.Column(db.Integer, db.ForeignKey('tree.tree_id'), nullable=False)
    url = db.Column(db.String)
    created = db.Column(db.DateTime)

    def __init__(self, tree_id, user_id, url):
        self.tree_id = tree_id
        self.user_id = user_id
        self.url = url
        self.created = datetime.utcnow()

    def to_dict(self):
        return {
            'id': self.id,
            'tree_id': self.tree_id,
            'user_id': self.user_id,
            'url': self.url,
            'created': self.created,
        }
