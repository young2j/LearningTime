from flask import Blueprint
api = Blueprint('api',__name__)

from . import httpauth,posts,users,comments,errors #一定要导入，否则无法注册路由！！！！！！！！！！！！！！