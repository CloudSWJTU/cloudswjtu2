from exts import db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
# 日记记录
class DiaryModel(db.Model, SerializerMixin):
    serialize_only = ("id", "content", "create_user", "create_time")
    __tablename__ = "diary"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    create_user=db.Column(db.Integer) #创建人
    create_time = db.Column(db.DateTime, default=datetime.now)


