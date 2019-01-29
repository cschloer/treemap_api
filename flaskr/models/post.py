from ..database import db
from datetime import datetime

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column('post_id', db.Integer, primary_key=True)
    user_id = db.Column(db.String(60), nullable=False)
    tree_id = db.Column(db.Integer, db.ForeignKey('tree.tree_id'), nullable=False)
    text = db.Column(db.String(1000))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)
    comments = db.relationship('PostComment')
    tree = db.relationship('Tree', back_populates='posts')

    def __init__(self, user_id, tree_id, text):
        self.user_id = user_id
        self.tree_id = tree_id
        self.text = text

    def to_dict(self, get_tree=True):
        comments = [comment.to_dict() for comment in self.comments]
        return_dict = {
            'id': self.id,
            'user_id': self.user_id,
            'tree_id': self.tree_id,
            'text': self.text,
            'created': self.created,
            'updated': self.updated,
            'comments': comments,
        }
        if get_tree:
            return_dict['tree'] = self.tree.to_dict()
        return return_dict
