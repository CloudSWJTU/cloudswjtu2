from exts import db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin


#
class UserModel(UserMixin,db.Model, SerializerMixin):
    serialize_only = ("id", "name", "email", "img")
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(20))
    img = db.Column(db.String(2000)) #头像
    password = db.Column(db.String(100))
    role=db.Column(db.Integer,default=0) #角色0:普通用户 1:管理员
    create_time = db.Column(db.DateTime, default=datetime.now)

class InterestModel(db.Model,SerializerMixin):
    serialize_only = ("id", "name")
    __tablename__ = "interest"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True)
class UserInterestModel(db.Model,SerializerMixin):
    serialize_only = ("id", "user_id", "interest_id")
    __tablename__ = "user_interest"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    interest_id = db.Column(db.Integer, db.ForeignKey("interest.id"))




