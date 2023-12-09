from datetime import datetime

from appdir import db


class Advs(db.Model):
    __tablename__ = 'advs'
    id = db.Column(db.Integer, primary_key=True)
    adv_title = db.Column(db.String(64), nullable=False, index=True)
    adv_image_route = db.Column(db.String(64))
    adv_time = db.Column(db.String(128))
    adv_content = db.Column(db.String)
    adv_category = db.Column(db.String(64))

