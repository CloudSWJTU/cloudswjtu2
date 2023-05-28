from flask import (
    Blueprint,
    request,
    render_template, redirect, url_for,
)
from flask_login import current_user, login_required
from sqlalchemy import or_

from exts import db
from utils import staticutils
from models.landmark import LandmarkModel
bp = Blueprint("landmark", __name__, url_prefix="/landmark")
from models.account import UserModel
@bp.route('/list', methods=['GET'])
@login_required
def landmakView():
    return render_template('swjtudb.html')

@bp.route("/message/list",methods=["GET"])
@login_required
def messagelistView():
    keyword=request.args.get("keyword")
    if keyword is  None or keyword.strip()=="":
        landmarkList=LandmarkModel.query.all()
    else:
        landmarkList=LandmarkModel.query.filter(or_(LandmarkModel.title.like("%{}%".format(keyword)),LandmarkModel.content.like("%{}%".format(keyword))))
    result=[]
    for i in landmarkList:
        dict1={}
        dict1["id"]=i.id
        dict1["title"]=i.title
        dict1["image"]=i.image
        dict1["content"]=i.content
        dict1["create_time"]=i.create_time
        try:
            dict1["create_user"]=UserModel.query.get(i.create_user).name
        except:
            continue
        result.append(dict1)



    return render_template('message.html',result=result)



@bp.route("/message/add",methods=["POST"])
@login_required
def messageAddView():
    title=request.form.get("title")
    image=request.files["image"]
    content=request.form.get("content")

    lm=LandmarkModel(title=title,content=content,image=staticutils.saveImage(image),create_user=current_user.id)
    db.session.add(lm)
    db.session.commit()
    return redirect(url_for('landmark.messagelistView'))