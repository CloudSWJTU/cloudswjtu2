from datetime import datetime

from flask import (
    Blueprint,
    request,
    render_template, jsonify,
)
from flask_login import login_required, current_user

from exts import db
from models.server import ServerModel
from utils.staticutils import saveImage

bp = Blueprint("server", __name__, url_prefix="/server")


@bp.route('/list', methods=['GET'])
@login_required
def serverView():
    serverModels=ServerModel.query.all()
    return render_template('fuwuquzhidao.html',serverModels=serverModels)



@bp.route('/upload', methods=['GET',"POST"])
@login_required
def serverUploadView():
    image= request.files["image"]
    name=request.form.get('name')
    serverModel = ServerModel(content=name, img=saveImage(image),create_user=current_user.id)
    db.session.add(serverModel)
    db.session.commit()
    return jsonify({"code":1,"info":"上传成功"})

@bp.route('/changename', methods=['GET',"POST"])
@login_required
def changeNameView():
    name= request.args.get("name")
    id= request.args.get("id")

    serverModel = ServerModel.query.get(id)
    serverModel.content=name
    db.session.add(serverModel)
    db.session.commit()
    return jsonify({"code":1,"info":"修改成功"})