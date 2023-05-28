from flask import (
    Blueprint,
    request,
    render_template, redirect, url_for,
)
from flask_login import current_user, login_required

from models.account import UserModel
from models.admin import VideoModel, LogModel
from models.history import HistoryModel
from models.landmark import LandmarkModel
from models.league import LeagueModel,ActivityModel,LeagueCateModel
from models.server import ServerModel
from utils.md5utils import get_md5_from_str
from utils.staticutils import saveImage

bp = Blueprint("admin", __name__, url_prefix="/admin")
from exts import db
# 对管理员的用户进行权限拦截
@bp.before_request
def checkurl():
    if current_user.role==0:
        return redirect("/")


@bp.route('/log/list', methods=['GET'])
@login_required
def LogListView():
    if request.method=="GET":
        page = request.args.get("page", 1)
        if page is None:
            page = 1
        else:
            page = int(page)
        keyword = request.args.get("keyword", None)
        logmodel=LogModel.query
        if keyword is not None:
            logmodel=logmodel.filter(LogModel.username.like('%'+keyword+"%"))
        logmodel=logmodel.all()
        start_index = (page - 1) * 10
        end_index = page * 10
        row_len = int(len(logmodel) / 10) + 1
        logmodel = logmodel[start_index:end_index]
        page_range = []
        for i in range(1, row_len + 1):
            page_range.append(i)
        for i in logmodel:
            print(i.type)



        return render_template('admin/admin_log_list.html',result=logmodel,page_range=page_range,page=page,keyword=keyword)

import os
@bp.route('/league/list', methods=['GET'])
@login_required
def LeagueListView():
    if request.method=="GET":
        page = request.args.get("page", 1)
        if page is None:
            page = 1
        else:
            page = int(page)
        keyword = request.args.get("keyword", None)
        leagueList=LeagueModel.query
        if keyword is not None:
            leagueList=leagueList.filter(LeagueModel.name.like('%'+keyword+"%"))
        leagueList=leagueList.all()
        start_index = (page - 1) * 10
        end_index = page * 10
        row_len = int(len(leagueList) / 10) + 1
        leagueList = leagueList[start_index:end_index]
        page_range = []
        for i in range(1, row_len + 1):
            page_range.append(i)
        result=[]
        for i in leagueList:
            dict1={}
            dict1['id']=i.id
            dict1['name']=i.name
            dict1['summary']=i.summary
            dict1['image']=i.image
            dict1['create']=i.create_time
            dict1['cate']=LeagueCateModel.query.get(i.cate).name
            result.append(dict1)



        return render_template('admin/admin_league_list.html',result=result,page_range=page_range,page=page,keyword=keyword)




@bp.route('/league/option', methods=['GET',"POST"])
@login_required
def LeagueAddView():
    id=request.args.get("id",None)
    leaguecagtes=LeagueCateModel.query.all()
    if id is not None:
        league = LeagueModel.query.get(id)
    else:
        league = None
    if request.method=="GET":
        return render_template('admin/admin_league_option.html',leaguecagtes=leaguecagtes,league=league)

    cate= request.form.get('cate')
    name= request.form.get('name')
    summary= request.form.get('summary')
    image= request.files["image"]

    if  image.filename!="":
        saveImage(image)
    if id is  None:
        league = LeagueModel(cate=cate, name=name, summary=summary, image="/static/img/"+image.filename)
    else:
        league.name=name
        league.summary=summary
        league.cate=cate
        if image.filename!="":
            league.image="/static/img/"+image.filename

    db.session.add(league)
    db.session.commit()
    return redirect(url_for('admin.LeagueListView'))

@bp.route('/league/del', methods=['GET',"POST"])
@login_required
def LeagueDelView():
    id=request.args.get("id")

    league = LeagueModel.query.get(id)
    db.session.delete(league)
    db.session.commit()
    return redirect(url_for('admin.LeagueListView'))


@bp.route('/server/list', methods=['GET'])
@login_required
def ServerListView():
    if request.method=="GET":
        page = request.args.get("page", 1)
        if page is None:
            page = 1
        else:
            page = int(page)
        keyword = request.args.get("keyword", None)
        data=ServerModel.query
        result=[]
        #     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        if keyword is not None:
            data = data.filter(ServerModel.content.like('%' + keyword + "%"))
        data = data.all()
        start_index = (page - 1) * 10
        end_index = page * 10
        row_len = int(len(data) / 10) + 1
        data = data[start_index:end_index]
        page_range = []
        for i in range(1, row_len + 1):
            page_range.append(i)
        for i in data:
            dict1={}
            dict1['id']=i.id
            dict1['content']=i.content
            dict1['image']=i.img
            try:
                dict1['create_user'] = UserModel.query.get(i.create_user).name
            except:
                continue

            result.append(dict1)



        return render_template('admin/admin_server_list.html',result=result,page_range=page_range,page=page,keyword=keyword)




@bp.route('/server/option', methods=['GET',"POST"])
@login_required
def ServerAddView():
    id=request.args.get("id",None)
    if id is not None:
        row = ServerModel.query.get(id)
    else:
        row = None
    if request.method=="GET":
        return render_template('admin/admin_server_option.html',row=row)

    content= request.form.get('content')
    image= request.files["image"]

    if  image.filename!="":
        saveImage(image)
        # image.save(r'./static/img/'+image.filename)
    if id is  None:
        row = ServerModel(content=content,img="/static/img/"+image.filename,create_user=current_user.id)
    else:
        row.name=content
        if image.filename!="":
            print(image.filename)
            row.img="/static/img/"+image.filename
    db.session.add(row)
    db.session.commit()
    return redirect(url_for('admin.ServerListView'))

@bp.route('/server/del', methods=['GET',"POST"])
@login_required
def ServerDelView():
    id=request.args.get("id")
    row = ServerModel.query.get(id)
    db.session.delete(row)
    db.session.commit()
    return redirect(url_for('admin.ServerListView'))




@bp.route('/history/list', methods=['GET'])
@login_required
def HistoryListView():
    if request.method=="GET":
        page = request.args.get("page", 1)
        if page is None:
            page = 1
        else:
            page = int(page)
        keyword = request.args.get("keyword", None)
        data=HistoryModel.query
        result=[]
        if keyword is not None:
            data = data.filter(HistoryModel.content.like('%' + keyword + "%"))
        data = data.all()
        start_index = (page - 1) * 10
        end_index = page * 10
        row_len = int(len(data) / 10) + 1
        data = data[start_index:end_index]
        page_range = []
        for i in range(1, row_len + 1):
            page_range.append(i)
        result = []

        for i in data:
            dict1={}
            dict1['id']=i.id
            dict1['content']=i.content
            dict1['image']=i.img
            dict1['create_time']=i.create_time
            try:
                dict1['create_user']=UserModel.query.get(i.create_user).name
            except:
                continue
            dict1['is_prioity']=i.is_prioity
            dict1['is_compliance']=i.is_compliance
            dict1['is_meaning']=i.is_meaning
            result.append(dict1)


        return render_template('admin/admin_history_list.html',result=result,page_range=page_range,page=page,keyword=keyword)




@bp.route('/history/option', methods=['GET',"POST"])
@login_required
def HistoryAddView():
    id=request.args.get("id",None)
    if id is not None:
        row = HistoryModel.query.get(id)
    else:
        row = None
    if request.method=="GET":

        return render_template('admin/admin_history_option.html',row=row)

    content= request.form.get('content')
    is_prioity= request.form.get('is_prioity')
    is_compliance= request.form.get('is_compliance')
    is_meaning= request.form.get('is_meaning')

    if is_prioity is not None and is_prioity=="on":
        is_prioity=1
    else:
        is_prioity=0
    if is_compliance is not None and is_compliance=="on":
        is_compliance=1
    else:
        is_compliance=0
    if is_meaning is not None and is_meaning=="on":
        is_meaning=1
    else:
        is_meaning=0
    image= request.files["image"]

    if  image.filename!="":
        saveImage(image)
        # image.save(r'./static/img/'+image.filename)
    if id is  None:
        row = HistoryModel(content=content,img="/static/img/"+image.filename,create_user=current_user.id,is_prioity=is_prioity,is_compliance=is_compliance,is_meaning=is_meaning)
    else:
        row.content=content
        if image.filename!="":
            row.img="/static/img/"+image.filename
        row.is_prioity=is_prioity
        row.is_compliance=is_compliance
        row.is_meaning=is_meaning

    db.session.add(row)
    db.session.commit()
    return redirect(url_for('admin.HistoryListView'))

@bp.route('/history/del', methods=['GET',"POST"])
@login_required
def HistoryDelView():
    id=request.args.get("id")
    row = HistoryModel.query.get(id)
    db.session.delete(row)
    db.session.commit()
    return redirect(url_for('admin.HistoryListView'))

#

@bp.route('/landmark/list', methods=['GET'])
@login_required
def LandmarkListView():
    if request.method=="GET":
        page = request.args.get("page", 1)
        if page is None:
            page = 1
        else:
            page = int(page)
        keyword = request.args.get("keyword", None)
        data=LandmarkModel.query
        result=[]
        if keyword is not None:
            data = data.filter(LandmarkModel.title.like('%' + keyword + "%"))
        data = data.all()
        start_index = (page - 1) * 10
        end_index = page * 10
        row_len = int(len(data) / 10) + 1
        data = data[start_index:end_index]
        page_range = []
        for i in range(1, row_len + 1):
            page_range.append(i)
        result = []

        for i in data:
            dict1={}
            dict1['id']=i.id
            dict1['title']=i.title
            dict1['content']=i.content
            dict1['create_time']=i.create_time
            dict1['image']=i.image
            try:
                dict1['create_user'] = UserModel.query.get(i.create_user).name
            except:
                continue
            result.append(dict1)


        return render_template('admin/admin_landmark_list.html',result=result,page_range=page_range,page=page,keyword=keyword)




@bp.route('/landmark/option', methods=['GET',"POST"])
@login_required
def LandmarkAddView():
    id=request.args.get("id",None)
    if id is not None:
        row = LandmarkModel.query.get(id)
    else:
        row = None
    if request.method=="GET":
        return render_template('admin/admin_landmark_option.html',row=row)

    content= request.form.get('content')
    title= request.form.get('title')
    image= request.files["image"]

    if  image.filename!="":
        saveImage(image)
        # image.save(r'./static/img/'+image.filename)
    if id is  None:
        row = LandmarkModel(content=content,image="/static/img/"+image.filename,title=title,create_user=current_user.id)
    else:
        row.content=content
        row.title=title
        if image.filename!="":
            row.image="/static/img/"+image.filename
    db.session.add(row)
    db.session.commit()
    return redirect(url_for('admin.LandmarkListView'))

@bp.route('/landmark/del', methods=['GET',"POST"])
@login_required
def LandmarkDelView():
    id=request.args.get("id")
    row = LandmarkModel.query.get(id)
    db.session.delete(row)
    db.session.commit()
    return redirect(url_for('admin.LandmarkListView'))



@bp.route('/activity/list', methods=['GET'])
@login_required
def ActivityListView():
    if request.method=="GET":
        data=ActivityModel.query.all()
        result=[]
        for i in data:
            dict1={}
            dict1['id']=i.id
            dict1['summary']=i.summary
            dict1['name']=i.name
            dict1['address']=i.address
            dict1['image']=i.image
            print(i.league_id)
            dict1['league']=LeagueModel.query.get(i.league_id).name
            try:
                dict1['create_user'] = UserModel.query.get(i.create_user).name
            except:
                continue
            result.append(dict1)
        return render_template('admin/admin_activity_list.html',result=result)




@bp.route('/activity/option', methods=['GET',"POST"])
@login_required
def ActivityAddView():
    id=request.args.get("id",None)
    leagues=LeagueModel.query.all()
    if id is not None:
        row = ActivityModel.query.get(id)
    else:
        row = None
    if request.method=="GET":
        return render_template('admin/admin_activity_option.html',row=row,leagues=leagues)

    summary= request.form.get('summary')
    name= request.form.get('name')
    address= request.form.get('address')
    league_id= request.form.get('league_id')
    image= request.files["image"]

    if  image.filename!="":
        saveImage(image)
        # image.save(r'./static/img/'+image.filename)
    if id is  None:
        row = ActivityModel(summary=summary,image="/static/img/"+image.filename,create_user=current_user.id,league_id=league_id,address=address,name=name)
    else:
        row.name=name
        row.summary=summary
        row.league_id=league_id
        row.address=address
        if image.filename!="":
            print(image.filename)
            row.img="/static/img/"+image.filename
    db.session.add(row)
    db.session.commit()
    return redirect(url_for('admin.ActivityListView'))

@bp.route('/activity/del', methods=['GET',"POST"])
@login_required
def ActivityDelView():
    id=request.args.get("id")
    row = ActivityModel.query.get(id)
    db.session.delete(row)
    db.session.commit()
    return redirect(url_for('admin.ActivityListView'))



@bp.route('/account/list', methods=['GET'])
@login_required
def AccountListView():
    if request.method=="GET":
        page=request.args.get("page",1)
        if page is None:
            page=1
        else:
            page=int(page)
        keyword=request.args.get("keyword",None)
        row=UserModel.query.filter(UserModel.role==0)
        if keyword is not None:
            row=row.filter(UserModel.name.like('%'+keyword+"%"))
        row=row.all()
        start_index=(page-1)*10
        end_index=page*10
        row_len=int(len(row)/10)+1
        row=row[start_index:end_index]
        page_range=[]
        for i in range(1,row_len+1):
            page_range.append(i)
        result=[]


        return render_template('admin/admin_account_list.html',result=row,page=page,page_range=page_range,keyword=keyword)




@bp.route('/account/option', methods=['GET',"POST"])
@login_required
def AccountAddView():
    id=request.args.get("id",None)
    if id is not None:
        row = UserModel.query.get(id)
    else:
        row = None
    if request.method=="GET":
        return render_template('admin/admin_account_option.html',row=row)

    name= request.form.get('name')
    email= request.form.get('email')
    password= request.form.get('password')

    image= request.files["image"]

    if  image.filename!="":
        saveImage(image)
        # image.save(r'./static/img/'+image.filename)
    if id is  None:
        userm=UserModel.query.filter(UserModel.name==name).first()
        if userm is not None:
            message="该用户名已经存在"
            return '<script>alert("该用户名已经存在！");location.href="/admin/account/option"</script>'
        userm=UserModel.query.filter(UserModel.email==email).first()
        if userm is not None:
            message="该邮箱已经存在"
            return '<script>alert("该邮箱已经存在！");location.href="/admin/account/option"</script>'

        row = UserModel(name=name,email=email,img="/static/img/"+image.filename,role=0,password=get_md5_from_str(password))
    else:
        usernm1=UserModel.query.get(id)
        userm = UserModel.query.filter(UserModel.name == name).first()

        print(userm is not None)
        if userm is not None and name!=usernm1.name:
            message = "该用户名已经存在"
            return '<script>alert("该用户名已经存在！");location.href="/admin/account/option?id={}"</script>'.format(id)
        userm = UserModel.query.filter(UserModel.email == email).first()
        if userm is not None and email!=usernm1.email:
            message = "该邮箱已经存在"
            return '<script>alert("该邮箱已经存在！");location.href="/admin/account/option?id={}"</script>'.format(id)

        row.name=name
        row.email=email
        if password is not None and password!="":
            row.password=get_md5_from_str(password)
        if image.filename!="":
            print(image.filename)
            row.img="/static/img/"+image.filename
    db.session.add(row)
    db.session.commit()
    return redirect(url_for('admin.AccountListView'))

@bp.route('/account/del', methods=['GET',"POST"])
@login_required
def AccountDelView():
    id=request.args.get("id")
    row = UserModel.query.get(id)
    db.session.delete(row)
    db.session.commit()
    return redirect(url_for('admin.AccountListView'))


@bp.route('/video/list', methods=['GET'])
@login_required
def VideoListView():
    if request.method=="GET":
        page=request.args.get("page",1)
        if page is None:
            page=1
        else:
            page=int(page)
        keyword=request.args.get("keyword",None)
        row=VideoModel.query
        if keyword is not None:
            row=row.filter(VideoModel.title.like('%'+keyword+"%"))
        row=row.all()
        for i in row:
            print(i.title,i.url)
        start_index=(page-1)*10
        end_index=page*10
        row_len=int(len(row)/10)+1
        row=row[start_index:end_index]
        page_range=[]
        for i in range(1,row_len+1):
            page_range.append(i)
        result=[]


        return render_template('admin/admin_video_list.html',result=row,page=page,page_range=page_range,keyword=keyword)




@bp.route('/video/option', methods=['GET',"POST"])
@login_required
def VideoAddView():
    id=request.args.get("id",None)
    if id is not None:
        row = VideoModel.query.get(id)
    else:
        row = None
    if request.method=="GET":
        return render_template('admin/admin_video_option.html',row=row)

    title= request.form.get('title')

    video= request.files["video"]

    if  video.filename!="":
        url=saveImage(video)
        # image.save(r'./static/img/'+image.filename)
    if id is None:
        row = VideoModel(title=title,url=url)
    else:
        row=VideoModel.query.get(id)


        row.title=title

        if video.filename!="":
            row.img="/static/img/"+video.filename
    db.session.add(row)
    db.session.commit()
    return redirect(url_for('admin.VideoListView'))

@bp.route('/video/del', methods=['GET',"POST"])
@login_required
def videoDelView():
    id=request.args.get("id")
    row = VideoModel.query.get(id)
    db.session.delete(row)
    db.session.commit()
    return redirect(url_for('admin.VideoListView'))

