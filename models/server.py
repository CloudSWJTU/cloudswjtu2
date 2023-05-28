from exts import db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

# 服务区图片
class ServerModel(db.Model, SerializerMixin):
    serialize_only = ("id", "name", "email", "img")
    __tablename__ = "server"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    img = db.Column(db.String(1000)) #图片
    create_user=db.Column(db.Integer) #创建人

#     收藏记录
class CollectModel(db.Model,SerializerMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    create_user=db.Column(db.Integer) #创建人
    server_id=db.Column(db.Integer)
    create_time = db.Column(db.DateTime, default=datetime.now)
    __tablename__ = "server_collection"
