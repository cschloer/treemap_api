from ..database import db
from datetime import datetime

class PostComment(db.Model):
    __tablename__ = 'post_comment'
    id = db.Column('post_comment_id', db.Integer, primary_key=True)
    user_id = db.Column(db.String(60), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), nullable=False)
    text = db.Column(db.String(1000))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)

    def __init__(self, user_id, post_id, text):
        self.user_id = user_id
        self.post_id = post_id
        self.text = text

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'post_id': self.post_id,
            'text': self.text,
            'created': self.created,
            'updated': self.updated,
        }
