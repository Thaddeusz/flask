from flask_sqlalchemy import SQLAlchemy # an api for multiple DB handling
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '3badce9f82d5d3567d83e489552ad555'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from web_app import routes