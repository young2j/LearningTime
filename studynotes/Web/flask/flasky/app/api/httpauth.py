from flask import g,jsonify
# from flask_login import current_user
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

from app.models import User
from . import api
from .errors import forbidden,unauthorized


@auth.verify_password
def verify_password(email_or_name_token,password):
    if email_or_name_token=='':
        return False
    if password=='':
        user = User.verify_auth_token(email_or_name_token)
        g.current_user = user
        g.token_used = True
        return g.current_user is not None
    
    user_by_name = User.query.filter_by(name=email_or_name_token).first()
    user_by_email = User.query.filter_by(email=email_or_name_token).first()
    user = user_by_name or user_by_email
    if not user:
        return False
    g.current_user= user
    g.token_used = False
    return user.verify_password(password)


@api.before_request
@auth.login_required
def before_request():
    # print('current_user:',current_user)
    if not g.current_user.is_anonymous and \
        not g.current_user.confirmed:
        return forbidden('Unconfirmed account.') #阻止已登陆但未认证的账户



@api.route('/token',methods=['POST'])
def get_token():
    if g.current_user.is_anonymous or g.token_used: #强制利用账户密码获得token,避免使用过期旧令牌
        return unauthorized('Invalid credentials')
    return jsonify(
        {'token':g.current_user.gen_auth_token(expiration=3600),
        'expiration':3600
        })
