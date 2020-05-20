from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy

from config import config

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
mail = Mail()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.login_view = 'auth.login' #访问受保护的页面时，将重定向到登录页面

def create_app(config_name):
    app = Flask(__name__)

    # 初始化配置
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # 初始化扩展
    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    
    # 初始化路由views
    from .views.errors import errors
    app.register_blueprint(errors)
    from .views.post import post
    app.register_blueprint(post)
    from .views.login import auth
    app.register_blueprint(auth,url_prefix='/auth')
    from .views.user import user
    app.register_blueprint(user,url_prefix='/user')

    from .api import api
    app.register_blueprint(api,url_prefix='/api')

    return app


