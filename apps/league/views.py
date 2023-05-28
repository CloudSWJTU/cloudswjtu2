from flask import (
    Blueprint,
    request,
    render_template, redirect, url_for,
)
from flask_login import current_user, login_required
from sqlalchemy import or_

from exts import db
from models.account import UserModel
from models.league import LeagueModel, ActivityModel, LeagueCateModel, MyCollectionModel
from utils import staticutils

bp = Blueprint("league", __name__, url_prefix="/league")

@bp.route('/index', methods=['GET'])
@login_required
def IndexView():
    return render_template('club_index1.html')

@bp.route('/detail/<int:pk>', methods=['GET'])
@login_required
def detailView(pk):
    cate=LeagueCateModel.query.get(pk)
    leagues=LeagueModel.query.filter(LeagueModel.cate==pk).all()
    results=[]
    #    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #     cate = db.Column(db.Integer)
    #     name = db.Column(db.String(64))
    #     summary = db.Column(db.String(4096))
    #     image=db.Column(db.String(4096))
    #     create_time = db.Column(db.DateTime, default=datetime.now)
    for i in leagues:
        dict1={}
        dict1['id']=i.id
        dict1['cate']=i.cate
        dict1['name']=i.name
        dict1['summary']=i.summary
        dict1['image']=i.image
        dict1['create_time']=i.create_time
        mycollectionModel=MyCollectionModel.query.filter(MyCollectionModel.league_id==i.id).filter(MyCollectionModel.user_id==current_user.id).first()
        if mycollectionModel is None:
            dict1['iscollection']=False
        else:
            dict1['iscollection'] = True
        results.append(dict1)
    cates=LeagueCateModel.query.all()
    cate_list=[]
    for i in cates:
        cate_num=LeagueModel.query.filter(LeagueModel.cate==i.id).count()
        cate_list.append({"id":i.id,"name":i.name,"num":cate_num})

    return render_template('club_detail.html',cate=cate,leagues=results,cate_list=cate_list)


@bp.route("/active/list",methods=["GET"])
@login_required
def ActivelistView():
    keyword=request.args.get("keyword")
    if keyword is  None or keyword.strip()=="":
        activeList=ActivityModel.query.all()
    else:
        activeList=ActivityModel.query.filter(or_(ActivityModel.name.like("%{}%".format(keyword)),ActivityModel.summary.like("%{}%".format(keyword))))
    result=[]


    for i in activeList:
        dict1={}
        dict1["id"]=i.id
        dict1["name"]=i.name
        dict1["image"]=i.image
        dict1["create_time"]=i.create_time
        dict1["summary"]=i.summary.strip()
        dict1["address"]=i.address
        dict1["league_name"]=LeagueModel.query.get(i.league_id).name
        dict1["create_user"]=UserModel.query.get(i.create_user).name
        result.append(dict1)
    leagues=LeagueModel.query.all()

    cates=LeagueCateModel.query.all()
    cate_list=[]
    for i in cates:
        cate_num = LeagueModel.query.filter(LeagueModel.cate == i.id).count()
        cate_list.append({"id": i.id, "name": i.name, "num": cate_num})

    return render_template('active.html',result=result,leagues=leagues,cate_list=cate_list)

@bp.route("/active/add",methods=["POST"])
@login_required
def ActiveAddView():
    name=request.form.get("name")
    image=request.files["image"]
    summary=request.form.get("summary")
    address=request.form.get("address")
    league_id=request.form.get("league_id")

    am=ActivityModel(name=name,summary=summary,address=address,league_id=league_id,image=staticutils.saveImage(image),create_user=current_user.id)
    db.session.add(am)
    db.session.commit()
    return redirect("/league/active/list")


# MyCollectionModel
@bp.route("/collection",methods=["GET"])
@login_required
def collectionLeagueView():
    id=request.args.get("id")
    cid=request.args.get("cid")
    mcm=MyCollectionModel.query.filter(MyCollectionModel.league_id==id).filter(MyCollectionModel.user_id==current_user.id).first()
    if mcm is None:
        mcm=MyCollectionModel(user_id=current_user.id,league_id=id)
        db.session.add(mcm)
        db.session.commit()
    else:
        db.session.delete(mcm)
        db.session.commit()
    return redirect("/league/detail/{}".format(cid))