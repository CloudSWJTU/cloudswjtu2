from flask import (
    Blueprint,
    request,
    render_template, redirect, url_for,
)
from flask_login import current_user, login_required

from models.account import UserModel
from models.history import HistoryModel
from models.landmark import LandmarkModel
from models.league import LeagueModel,ActivityModel,LeagueCateModel
from models.server import ServerModel
from utils.md5utils import get_md5_from_str

bp = Blueprint("index", __name__, url_prefix="/index")
from exts import db

@bp.route("/indextest",methods=["GET"])
def indextest():
        return render_template("indextest.html")
