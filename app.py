import json

from flask import Flask, redirect, jsonify, request
from flask_login import current_user

import config
from exts import db, cors,login_manager,mail
from flask_migrate import Migrate
from apps.account import account_bp
from apps.admin import admin_bp
from apps.history import history_bp
from apps.landmark import landmark_bp
from apps.league import league_bp
from apps.server import server_bp
from apps.index import index_bp
from models.admin import LogModel

app = Flask(__name__)
app.config.from_object(config)
app.config['SECRET_KEY'] = 'wgwe2345h443cewg4he3'

db.init_app(app)
from models.league import LeagueCateModel
@app.context_processor
def inject_list():
    catelist=LeagueCateModel.query.all()
    cates=[]
    for i in catelist:
        cates.append({"id":i.id,"name":i.name})
    return dict(cates=cates)

    # return catelist
cors.init_app(app, origins="*")
from models.account import UserModel
login_manager.init_app(app)
login_manager.login_view = "account.loginAndCreate"
mail.init_app(app)
@app.route("/")
def index():
    return redirect("/index/indextest")
@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(user_id)
@app.before_request
def logInfo():
    if 'static' not in request.url:

        username="暂未登录"
        try:
            username=current_user.name
        except:
            pass
        if request.method=="GET":
            params=dict(request.args)
        else:
            params=dict(request.form)
        params=json.dumps(params)
        lm=LogModel(username=username,url=request.url,ip=request.remote_addr,type=request.method,params=params,flag=request.headers.get("User-Agent"))
        db.session.add(lm)
        db.session.commit()


migrate = Migrate(app, db)

# 注册蓝图
app.register_blueprint(account_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(landmark_bp)
app.register_blueprint(history_bp)
app.register_blueprint(league_bp)
app.register_blueprint(server_bp)
app.register_blueprint(index_bp)

if __name__ == '__main__':
    app.run(debug=True,port=5002)
