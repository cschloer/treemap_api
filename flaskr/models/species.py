from ..database import db
from datetime import datetime

class Species(db.Model):
    __tablename__ = 'species'
    id = db.Column('species_id', db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(200))
    created = db.Column(db.DateTime)

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.created = datetime.utcnow()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created': self.created,
        }
