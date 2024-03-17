from app import db
from datetime import datetime


class GreenhouseSensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gh_id = db.Column(db.String(3), nullable=False)
    sensor_id = db.Column(db.String(3), nullable=False)
    dht_temp = db.Column(db.Float, nullable=False)
    dht_humidity = db.Column(db.Float, nullable=False)
    ntc_temp = db.Column(db.Float, nullable=False)
    ldr_lux = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=lambda: datetime.now())
