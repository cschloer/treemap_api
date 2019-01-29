from ..database import db
from datetime import datetime

class Species(db.Model):
    __tablename__ = 'species'
    id = db.Column('species_id', db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    latin_name = db.Column(db.String(60))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    urls = db.relationship('SpeciesUrl')

    def __init__(self, name, latin_name):
        self.name = name
        self.latin_name = latin_name

    def to_dict(self):
        urls = [url.to_dict() for url in self.urls]
        return {
            'id': self.id,
            'name': self.name,
            'latin_name': self.latin_name,
            'created': self.created,
            'urls': urls,
        }
