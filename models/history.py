from exts import db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
# 历史照片
class HistoryModel(db.Model, SerializerMixin):
    serialize_only = ("id", "name", "email", "img")
    __tablename__ = "history"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    img = db.Column(db.String(1000)) #图片
    create_user=db.Column(db.Integer) #创建人
    is_prioity=db.Column(db.Integer,default=0) #是否优先
    is_compliance=db.Column(db.Integer,default=1) #是否合规
    is_meaning=db.Column(db.Integer,default=0) #是否有特殊含义
    create_time = db.Column(db.DateTime, default=datetime.now)



