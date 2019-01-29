from ..database import db
from datetime import datetime

class SpeciesUrl(db.Model):
    __tablename__ = 'species_url'
    id = db.Column('species_url_id', db.Integer, primary_key=True)
    species_id = db.Column(db.Integer, db.ForeignKey('species.species_id'), nullable=False)
    url = db.Column(db.String(1000))
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, species_id, url):
        self.species_id = species_id
        self.url = url

    def to_dict(self):
        return {
            'id': self.id,
            'species_id': self.species_id,
            'url': self.url,
            'created': self.created,
        }
