from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_babel import Babel
from manager.lib.JsonDB import JsonDB
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = SQLAlchemy()
csrf = CSRFProtect()
mail = Mail()
login_manager = LoginManager()
babel = Babel()
limiter = Limiter(key_func=get_remote_address)
f_db = JsonDB.JsonDB("Front_DB")