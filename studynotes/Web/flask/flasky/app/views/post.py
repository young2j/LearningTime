from flask import render_template,redirect,url_for,Blueprint,request,flash,abort,make_response,current_app
post = Blueprint('post',__name__)

from flask_login import current_user,login_required

from app.models import Permission, Post,Comment
from app import db
from .forms import PostForm, CommentForm
from app.decorators import permissions_required,admin_required

@post.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post = Post(body=form.body.data,author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('post.index'))

    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed','1'))
    else:
        show_followed = False

    if show_followed:
        query = current_user.followed_posts_query
    else:
        query = Post.query
    current_page = request.args.get('page',1,type=int) #默认第一页
    pagination = query.order_by(Post.timestamp.desc()).paginate(
                                        current_page,per_page=5,error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts,
                           pagination=pagination,show_followed=show_followed)


@post.route('/all')
@login_required
def show_all():
    response = make_response(redirect(url_for('post.index')))
    response.set_cookie('show_followed','',max_age=30*24*60*60)
    return response

@post.route('/show-followed')
def show_followed():
    response = make_response(redirect(url_for('post.index')))
    response.set_cookie('show_followed','1',max_age=30*24*60*60)
    return response

#==================================================================================================
@post.route('/post/<int:id>',methods=['GET','POST'])
def the_post(id):
    form = CommentForm()
    the_post = Post.query.get_or_404(id)
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          author=current_user._get_current_object(),
                          post=the_post)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('post.the_post',id=the_post.id,page=-1))

    current_page = request.args.get('page',1,type=int)
    if current_page==-1:
        current_page = (the_post.comments.count()-1)//5 + 1
    pagination = the_post.comments.order_by(Comment.timestamp.asc()).paginate(
                    current_page,per_page=5,error_out=False
                )
    comments = pagination.items
    return render_template('the_post.html',post=the_post,
                           form=form,pagination=pagination,
                           comments=comments)

#============================================================================
@post.route('/enable-comment/<id>')
@permissions_required(Permission.MODERATE)
def enable_comment(id):
    comment = Comment.query.filter_by(id=id).first()
    if not comment.disabled:
        flash('The comment is already enabled.')
    else:
        comment.disabled = False
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('post.the_post',id=comment.post_id,page=request.args.get('page',1,type=int)))

@post.route('/disable-comment/<id>')
@permissions_required(Permission.MODERATE)
def disable_comment(id):
    comment = Comment.query.filter_by(id=id).first()
    if comment.disabled:
        flash('The comment is already disabled.')
    else:
        comment.disabled = True
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('post.the_post',id=comment.post_id,page=request.args.get('page',1,type=int)))


#===============================================================================
@post.route('/moderate')
@permissions_required(Permission.MODERATE)
def moderate():
    current_page = request.args.get('page',1,type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
                    current_page,per_page=5,error_out=False
                )
    comments = pagination.items
    coments_num_not_disabled = Comment.query.filter_by(disabled=False).count()
    return render_template('moderate.html',
                           pagination=pagination,comments=comments,
                           comments_num_not_disabled = coments_num_not_disabled
                           )

@post.route('/moderate/<id>')
@permissions_required(Permission.MODERATE)
def moderate_enable(id):
    comment = Comment.query.filter_by(id=id).first()
    enable = bool(request.args.get('enable',1,type=int))
    if  enable:
        comment.disabled = False
    else:
        comment.disabled = True
    db.session.add(comment)
    db.session.commit()

    return redirect(url_for('post.moderate',page=request.args.get('page',1,type=int)))

#==================================================================================================
@post.route('/edit-post/<int:id>',methods=['GET','POST'])
@login_required
def edit_post(id):
    form = PostForm()
    post = Post.query.get_or_404(id)
    if form.validate_on_submit():
        if current_user!=post.author or not current_user.can(Permission.ADMIN):
            abort(403)
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('The post has been updated.')
        return redirect(url_for('post.the_post',id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html',form=form)

#=======================================================================================================

@post.app_context_processor
def inject_permission():
    return dict(Permission=Permission)

#=======================================================================================================
from flask_sqlalchemy import get_debug_queries

@post.after_app_request
def get_slow_query(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                "Slow query:%s\n,Parameters:%s\n,Duration:%s\n,Context:%s" % (
                    query.statement,
                    query.parameters,
                    query.duration,
                    query.context
                )
            )
    return response