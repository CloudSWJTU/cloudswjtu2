from exts import db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

class LeagueCateModel(db.Model,SerializerMixin):
    serialize_only = ("id", "name")
    __tablename__ = "league_cate"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True)
class LeagueModel(db.Model, SerializerMixin):
    serialize_only = ("id", "type", "name", "summary","image","create_time")
    __tablename__ = "leagud"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cate = db.Column(db.Integer)
    name = db.Column(db.String(64))
    summary = db.Column(db.String(4096))
    image=db.Column(db.String(4096))
    create_time = db.Column(db.DateTime, default=datetime.now)

class ActivityModel(db.Model,SerializerMixin):
    serialize_only = ("id", "address", "name", "summary","league_id","create_time")

    __tablename__ = "activity"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    image = db.Column(db.String(1024))
    create_time = db.Column(db.DateTime, default=datetime.now)
    summary = db.Column(db.String(4096))
    address=db.Column(db.String(4096))
    league_id=db.Column(db.Integer) #所属社团
    create_user=db.Column(db.Integer)
class MyCollectionModel(db.Model,SerializerMixin):

    __tablename__ = "league_collection"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    league_id = db.Column(db.Integer)





