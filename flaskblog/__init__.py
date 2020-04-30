from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv
from flaskblog.config import Config
from flask_restplus import Api

load_dotenv()

db = SQLAlchemy()
bcrypt = Bcrypt()
api = Api()
login_manager = LoginManager()
# login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    api.init_app(app)

    from flaskblog.restplus_users.routes import user_namespace
    from flaskblog.restplus_posts.routes import post_namespace
    app.register_blueprint(user_namespace)
    app.register_blueprint(post_namespace)

    return app
