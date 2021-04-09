from flask_sqlalchemy import SQLAlchemy # an api for multiple DB handling
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from web_app.config import config



db = SQLAlchemy()
bcrypt = Bcrypt()


login_manager = LoginManager()
login_manager.login_view = "users.login" # calls this is account is called
login_manager.login_message_category = "info"

mail = Mail() # flask email

    



def create_app(config_class=config):
    app = Flask(__name__)
    app.config.from_object(config) # this is where the config file is called

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from web_app.users.routes import users
    from web_app.posts.routes import posts
    from web_app.main.routes import main
    from web_app.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app