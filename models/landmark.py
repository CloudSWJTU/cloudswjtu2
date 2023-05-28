from exts import db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
class LandmarkModel(db.Model,SerializerMixin):
    serialize_only = ("id", "image", "title", "content","create_user","create_time")

    __tablename__ = "landmark"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(2048))
    create_time = db.Column(db.DateTime, default=datetime.now)
    image = db.Column(db.String(4096))
    content=db.Column(db.Text)
    create_user=db.Column(db.Integer)

