# flask_sqlalchemy
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager

db = SQLAlchemy()
cors = CORS()
login_manager = LoginManager()
mail=Mail()

