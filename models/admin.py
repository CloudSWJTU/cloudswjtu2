from exts import db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin


class VideoModel(db.Model,SerializerMixin):

    __tablename__ = "video"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(2048))
    create_time = db.Column(db.DateTime, default=datetime.now)
    url = db.Column(db.String(4096))
class LogModel(db.Model,SerializerMixin):
    __tablename__='log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username=db.Column(db.String(1000))
    create_time = db.Column(db.DateTime, default=datetime.now)
    url=db.Column(db.String(1000))
    type=db.Column(db.String(1000))
    params=db.Column(db.String(1000))
    flag=db.Column(db.String(1000))
    ip=db.Column(db.String(1000))