from flask import (
    Blueprint,
    request,
    render_template, jsonify,
)
from flask_login import current_user, login_required
from datetime import datetime

from exts import db
from models.history import HistoryModel
from utils.staticutils import saveImage

bp = Blueprint("history", __name__, url_prefix="/history")
@bp.route('/list', methods=['GET'])
@login_required
def historyView():
    historyLists=HistoryModel.query.all()


    return render_template('jdhistory.html',historyList=historyLists)

@bp.route('/list2', methods=['GET'])
@login_required
def history2View():
    historyLists=HistoryModel.query.all()


    return render_template('jdhistory2.html',historyList=historyLists)
# upload

@bp.route('/upload', methods=['GET',"POST"])
@login_required
def historyUploadView():
    image= request.files["image"]
    name=request.form.get('name')
    image.save(r'./static/img/' + image.filename)
    history = HistoryModel(content=name,  img="/static/img/" + image.filename,create_time=datetime.now(),create_user=current_user.id)
    db.session.add(history)
    db.session.commit()
    return jsonify({"code":1,"info":"上传成功"})