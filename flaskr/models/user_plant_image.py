from ..database import db
from datetime import datetime

class UserPlantImage(db.Model):
    __tablename__ = 'userplantimage'
    id = db.Column('user_plant_image_id', db.Integer, primary_key=True)
    user_plant_id = db.Column(db.Integer, db.ForeignKey('userplant.user_plant_id'), nullable=False)
    url = db.Column(db.String)
    created = db.Column(db.DateTime)

    def __init__(self, user_plant_id, url):
        self.user_plant_id = user_plant_id
        self.url = url
        self.created = datetime.utcnow()

    def to_dict(self):
        return {
            'id': self.id,
            'user_plant_id': self.user_plant_id,
            'url': self.url,
            'created': self.created,
        }
