from flask import request,g,jsonify,url_for
from wtforms.validators import ValidationError

from . import api
from app import db
from app.models import Post,Permission,Comment
from .errors import forbidden
from .decorators import permissions_required

#================get====================
@api.route('/posts/')
def get_posts():
    # posts = Post.query.all()
    # return jsonify([post.to_json() for post in posts])
    page = request.args.get('page',1,type=int)
    pagination = Post.query.paginate(page,per_page=5,error_out=False)
    posts = pagination.items
    
    prev_url = url_for('api.get_posts', page=page-1) if pagination.has_prev else None
    next_url = url_for('api.get_posts', page=page+1) if pagination.has_next else None

    return jsonify({
        'page':page,
        'posts':[post.to_json() for post in posts],
        'next_url':next_url,
        'prev_url':prev_url
    })

@api.route('/posts/<int:id>')
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify(post.to_json())

@api.route('/posts/<int:id>/comments')
def get_post_comments(id):
    post = Post.query.get_or_404(id)
    return jsonify([comment.to_json() for comment in post.comments])


#===============post=======================
@api.route('/posts/',methods=['POST'])
@permissions_required(Permission.WRITE)
def new_post():
    '''
    print('resquest_get_json:',request.get_json(force=True)) #raw
    print('form:',request.form.get('a')) #form-data
    '''
    post = Post.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json())

@api.route('/posts/<int:id>/comments',methods=['POST'])
@permissions_required(Permission.COMMENT)
def write_a_comment(id):
    post = Post.query.get_or_404(id)
    comment = Comment.from_json(request.json)
    comment.author = g.current_user
    comment.post = post
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_json())

#=================put==============================
@api.route('/posts/<int:id>',methods=['PUT'])
def modify_post(id):
    post = Post.query.get_or_404(id)
    if g.current_user!=post.author or not g.current_user.can(Permission.ADMIN):
        return forbidden('Insuficient Permission.')
    post.body = request.json.get('body',post.body)
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json())

'''
@api.errorhandler(ValidationError) # api中任何地方只要触发ValidationError就会返回此view,接受Exception类
def validation_error(e):
    return bad_request(e.args[0])
'''
