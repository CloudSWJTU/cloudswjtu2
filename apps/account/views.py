from flask import (
    Blueprint,
    request,
    render_template, jsonify, redirect,
)
from flask_login import login_user, current_user, login_required, logout_user
from flask_mail import Message

from exts import db, mail
from models.account import UserModel,InterestModel,UserInterestModel
from models.diary import DiaryModel
from utils.md5utils import get_md5_from_str

bp = Blueprint("account", __name__, url_prefix="/account")
key = '842400ba12604dcab4b694ce883a5b6c'
import requests
from utils.staticutils import saveImage
@bp.route("/login",methods=["GET","POST"])
def loginAndCreate():
    if request.method == "GET":
        interests=InterestModel.query.all()

        return render_template('login.html',interests=interests)
    else:
        type = request.args.get("type")
        # 如果是登陆，则进行以下处理
        if type == "login":
            email = request.form.get("email")
            password = request.form.get("password")
            print(password)
            password=get_md5_from_str(password)
            print(password)
            userModel=UserModel.query.filter_by(email=email,password=password).first()
            if userModel is None:
                return jsonify({"code":0,"info":"用户名或密码错误"})
            login_user(userModel)
            return jsonify({"code":1,"info":"登陆成功","role":userModel.role})
        else:
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")
            interest = request.values.getlist("interest[]")
            password=get_md5_from_str(password)
            userModel=UserModel.query.filter_by(email=email).first()
            if userModel is not None:
                return jsonify({"code":0,"info":"用户名已存在"})
            userModel=UserModel(name=username,email=email,password=password)
            db.session.add(userModel)


            userModel=UserModel.query.filter_by(email=email).first()

            for i in interest:
                interest_id=int(i)
                userInterestModel=UserInterestModel(interest_id=interest_id,user_id=userModel.id)
                db.session.add(userInterestModel)
            db.session.commit()
            return jsonify({"code":1,"info":"注册成功"})
import random
@bp.route("/person/")
@login_required
def person():
    keyword=request.args.get("keyword",None)
    diarylist=DiaryModel.query.filter(DiaryModel.create_user==current_user.id)
    if keyword is not None:
        keyword=keyword.strip()
        diarylist=diarylist.filter(DiaryModel.content.like('%'+keyword+"%"))
    UserInfo=UserModel.query.get(current_user.id)
    uim=UserInterestModel.query.filter(UserInterestModel.user_id==current_user.id)
    interestlist=[]
    for i in uim:
        interestlist.append(InterestModel.query.get(i.interest_id).name)
    interests=",".join(interestlist)
    if UserInfo.img is not None:
        avter=UserInfo.img+"?random={}".format(random.randint(10000,999999))
    else:
        avter=None

    # 获取城市id
    # 调用和风天气
    weather_url = f'https://devapi.qweather.com/v7/weather/now?key={key}&location=101270101'
    headers = {
        'Connection': 'close'
    }
    response = requests.get(weather_url,headers=headers)



    # 解析结果,将选哟的数据解析出来
    weather=None
    if response.status_code == 200:
        data = response.json()['now']
        weather={}
        weather['text']=data['text']
        weather['windDir']=data['windDir']
        weather['temp']=data['temp']
        weather['name']='成都'


    return render_template('person.html',diarylist=diarylist,interests=interests,UserInfo=UserInfo,avter=avter,weather=weather,keyword=keyword)


@bp.route("/editperson/",methods=['GET',"POST"])
@login_required
def editperson():
    if request.method=="GET":
        id=request.args.get("id",None)
        diary=DiaryModel.query.filter(DiaryModel.id==id).first()

        UserInfo=UserModel.query.get(current_user.id)
        uim=UserInterestModel.query.filter(UserInterestModel.user_id==current_user.id)
        interestlist=[]
        for i in uim:
            interestlist.append(InterestModel.query.get(i.interest_id).name)
        interests=",".join(interestlist)
        if UserInfo.img is not None:
            avter=UserInfo.img+"?random={}".format(random.randint(10000,999999))
        else:
            avter=None


        return render_template('edit_person.html',interests=interests,UserInfo=UserInfo,avter=avter,diary=diary)
    else:
        id=request.form.get("id",None)
        content=request.form.get("content",None)
        diaryModel=DiaryModel.query.get(id)
        diaryModel.content=content
        db.session.add(diaryModel)
        db.session.commit()
        return redirect("/account/person/")

@bp.route("/changepassword",methods=['GET',"POST"])
@login_required
def changepassword():
    UserInfo=UserModel.query.get(current_user.id)
    password=request.form.get("password")
    password2=request.form.get("password2")
    if password2!=password:
        return '<script>alert("两次密码不一致！");location.href="/account/person/"</script>'
    new_password=get_md5_from_str(password)
    UserInfo.password=new_password
    db.session.add(UserInfo)
    db.session.commit()
    return redirect("/account/person")


@bp.route("/upload", methods=['GET', "POST"])
@login_required
def uploadAvter():
    image=request.files["image"]

    UserInfo=UserModel.query.get(current_user.id)
    UserInfo.img=saveImage(image)
    db.session.add(UserInfo)
    db.session.commit()



    return jsonify({"code":1})


@bp.route("/changeInfo",methods=['GET',"POST"])
@login_required
def changeInfo():
    UserInfo = UserModel.query.get(current_user.id)
    email = request.form.get("email")
    name = request.form.get("name")
    print(email)
    if email is not None and email.strip()!="" and email!=current_user.email:
        ui=UserInfo.query.filter(UserInfo.email==email).first()
        if ui is not None:
            return '<script>alert("邮箱已注册！");location.href="/account/person/"</script>'
        else:
            UserInfo.email=email
    if name is not None and name.strip()!="" and name != current_user.name:
        ui = UserInfo.query.filter(UserInfo.name==name).first()
        if ui is not None:
            return '<script>alert("账号已注册！");location.href="/account/person/"</script>'
        else:
            UserInfo.name=name

    db.session.add(UserInfo)
    db.session.commit()

    return redirect("/account/person")
@bp.route("/daily/del")
@login_required
def deldaily():
    id=request.args.get("id")
    diaryid= DiaryModel.query.get(id)
    db.session.delete(diaryid)
    db.session.commit()

    return redirect("/account/person")


@bp.route("/daily/add",methods=["POST"])
@login_required
def adddaily():
    content=request.form.get("content")

    diaryid= DiaryModel(content=content,create_user=current_user.id)
    db.session.add(diaryid)
    db.session.commit()

    return redirect("/account/person")

import random
@bp.route("/send")
def sendemail():
    email=request.args.get("email")
    try:
        code=random.randint(1000,9999)
        msg = Message(subject="验证码",
                      recipients=[email])

        msg.body="您的验证码是：{}".format(code)
        mail.send(msg)

        return jsonify({"code":1,"data":code})
    except:
        return jsonify({"code":0})

@bp.route("/logout",methods=["GET","POST"])
def logoutNow():
    logout_user()
    return redirect("/account/login")
