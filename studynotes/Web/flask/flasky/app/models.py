import hashlib
from datetime import datetime

import bleach
from flask import current_app, request,url_for
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import markdown
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import ValidationError

from app import db, login_manager


#====================================================================================================

class Permission:
    FOLLOW = 1 # 关注用户
    COMMENT = 2 # 评论
    WRITE = 4 # 写
    MODERATE =8 # 助管
    ADMIN = 16 # 超管


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean,default=False,index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self,**kwargs):
        super(Role,self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def add_permission(self,perm):
        if not self.has_permission(perm):
            self.permissions+=perm
    
    def remove_permission(self,perm):
        if self.has_permission(perm):
            self.permissions-=perm
        else:
            print('There not exists the permission.')
    
    def reset_permission(self):
        self.permissions = 0
    
    def has_permission(self,perm):
        return self.permissions & perm==perm

    # shell
    @staticmethod
    def insert_roles():
        roles = {
            'User':[Permission.FOLLOW,Permission.COMMENT,
                    Permission.WRITE],
            'Moderator':[Permission.FOLLOW,Permission.COMMENT,
                         Permission.WRITE,Permission.MODERATE],
            'Administrator':[Permission.FOLLOW,Permission.COMMENT,
                             Permission.WRITE,Permission.MODERATE,
                             Permission.ADMIN]
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permission()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name==default_role)
            db.session.add(role)
        db.session.commit()
        
    def __repr__(self):
        return '<Role %r>' % self.name

#====================================================================================================
class Follow(db.Model): #关联表：自引用
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer,db.ForeignKey('users.id'),primary_key=True)
    followed_id = db.Column(db.Integer,db.ForeignKey('users.id'),primary_key=True)
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean,default=False)
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(),default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(),default=datetime.utcnow) # 每次发起请求都要刷新最后访问时间
    avatar_hash = db.Column(db.String(32)) #头像hash值
    #-------
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    #-------
    posts = db.relationship('Post',backref='author',lazy='dynamic')  #lazy都在‘一’侧，返回的结果是‘多’侧
    #-------
    followed = db.relationship('Follow',foreign_keys=[Follow.follower_id],
                               backref = db.backref('follower',lazy='joined'),
                               lazy='dynamic',
                               cascade = 'all,delete-orphan'
                               ) #user关注的人
    follower = db.relationship('Follow',foreign_keys=[Follow.followed_id],
                               backref = db.backref('followed',lazy='joined'),
                               lazy='dynamic',
                               cascade = 'all,delete-orphan'
                               ) #关注user的人

    #-------
    comments = db.relationship('Comment',backref='author',lazy='dynamic')

    #-------
    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            else:
                self.role = Role.query.filter_by(default=True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = self.gen_avatar_hash()

        self.follow(self) #自己关注自己,以便首页能显示自己的文章

    #-------
    # 查询用户权限
    def can(self,perm):
        return self.role is not None and self.role.has_permission(perm)
    
    def is_administrator(self):
        return self.can(Permission.ADMIN)

    #-------
    # 密码设置和验证
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')
    
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def generate_confirmation_token(self,expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'],expires_in=expiration)
        return s.dumps({'confirm':self.id}).decode('utf-8')
    
    def confirm(self,token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True
    #-------发起api请求的令牌验证-----------
    def generate_auth_token(self,expiration):
        s = Serializer(current_app.config['SECRET_KEY'],expires_in=expiration)
        return s.dumps({'id':self.id}).decode('utf-8')
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return None
        return User.query.get(data.get('id'))            
    #-------
    # 刷新访问时间
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    #-------
    #根据邮箱生成头像的hash值
    def gen_avatar_hash(self): 
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def get_avatar(self,size=100,default='identicon',rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        
        if self.email is not None:
            avatar_hash = self.avatar_hash or self.gen_avatar_hash() 
        else:
            avatar_hash = 'cb1f01c6f143ab38ec06cca4f59e4802'
        return '{url}/{avatar_hash}?s={size}&d={default}&r={rating}'.format(
            url=url,avatar_hash=avatar_hash,size=size,default=default,rating=rating
        )

    #-------
    def is_following(self,user): #正在关注
        if user.id is None:
            return False
        return  self.followed.filter_by(followed_id=user.id).first() is not None

    def is_followed_by(self,user): #被谁关注
        if user.id is None:
            return False
        return  self.follower.filter_by(follower_id=user.id).first() is not None

    def follow(self,user): #关注
        if not self.is_following(user):
            f = Follow(follower=self,followed=user)
            db.session.add(f)

    def unfollow(self,user):#取关
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)
    #--------------
    @property
    def followed_posts_query(self):
        # query = db.session.query(Post)\
        #         .select_from(Follow).filter_by(follower_id=self.id)\
        #         .join(Post,Follow.followed_id==Post.author_id) #
        query = Post.query.join(Follow,Follow.followed_id==Post.author_id)\
                .filter(Follow.follower_id==self.id) #等价的
        return query

    #自关注shell
    @staticmethod
    def follow_self():
        users = User.query.all()
        for u in users:
            if not u.is_following(u):
                u.follow(u)
                db.session.add(u)
                db.session.commit()
    
    #api
    def to_json(self):
        user_json = {
            'username':self.name,
            'role':self.role.name,
            "member_since":self.member_since,
            "last_seen":self.last_seen,
            'url':url_for('api.get_user',id=self.id),
            "posts_url":url_for('api.get_user_posts',id=self.id),
            'posts_count':self.posts.count(),
            'followed_posts_url':url_for('api.get_followed_posts',id=self.id),
        }
        return user_json


    def __repr__(self):
        return '<User %r>' % self.name

class AnonymousUser(AnonymousUserMixin):
    
    def can(self,perm):
        return False

    def is_administrator(self):
        return False
login_manager.anonymous_user = AnonymousUser #使用匿名用户类，无须检查用户是否登录，就可以调用current_user.can()和current_user.is_administrator()

@login_manager.user_loader #注册到flask_login扩展，在扩展需要获取已登录用户的信息时调用【为模板中的current_user赋值】
def load_user(user_id):
    return User.query.get(int(user_id))

#====================================================================================================

class Post(db.Model):
    __tablename__='posts'
    id = db.Column(db.Integer,primary_key=True)
    body=db.Column(db.Text)
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    body_html = db.Column(db.Text())

    comments = db.relationship('Comment',backref='post',lazy='dynamic')

    @staticmethod
    def on_changed_body(target,value,oldvalue,initiator):
       target.body_html =  bleach.linkify(
                            bleach.clean(
                                markdown(value,output_format='html'),strip=True)
                        )
    # api
    def to_json(self):
        post_json = {
            'id':self.id,
            'url':url_for('api.get_post',id=self.id),
            'body':self.body,
            'body_html':self.body_html,
            'timestamp':self.timestamp,
            'author_url':url_for('api.get_user',id=self.author_id),
            'comments_url':url_for('api.get_post_comments',id=self.id),
            'comments_count':self.comments.count()
        }
        return post_json

    # api
    @staticmethod
    def from_json(post_json):
        body = post_json.get('body')
        if body is None or body=='':
            raise ValidationError('post does not have a body.')
        return Post(body=body)


db.event.listen(Post.body,'set',Post.on_changed_body)

#====================================================================================================

class Comment(db.Model):
    __tablename__='comments'
    id = db.Column(db.Integer,primary_key=True)
    body=db.Column(db.Text)
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'))
    body_html = db.Column(db.Text)
    disabled = db.Column(db.Boolean,default=False)

    @staticmethod
    def on_changed_body(target,value,oldvalue,initiator):
       target.body_html =  bleach.linkify(
                            bleach.clean(
                                markdown(value,output_format='html'),strip=True)
                        )
    
    #api
    def to_json(self):
        comment_json = {
            'id':self.id,
            'post_id':self.post_id,
            'author_id':self.author_id,
            'body':self.body,
            'body_html':self.body_html,
            'timestamp':self.timestamp,
            'disabled':self.disabled,
            'url':url_for('api.get_comment',id=self.id),
            'author_url':url_for('api.get_user',id=self.author_id),
            'post_url':url_for('api.get_post',id=self.post_id)
        }
        return comment_json

    # api
    @staticmethod
    def from_json(comment_json):
        body = comment_json.get('body')
        if body is None or body == '':
            raise ValidationError('comment does not have a body.')
        return Comment(body=body)

db.event.listen(Comment.body,'set',Comment.on_changed_body)
