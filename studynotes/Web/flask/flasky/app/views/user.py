from flask import Blueprint,render_template,flash,redirect,url_for,request
user = Blueprint('user',__name__)

from flask_login import login_required,current_user
import hashlib

from app.models import User,Post,Permission
from app import db
from .forms import EditProfileForm,EditProfileForAdminForm
from app.decorators import admin_required,permissions_required


@user.route('/<username>')
@login_required
def user_info(username):
    user = User.query.filter_by(name=username).first_or_404()
    # posts = user.posts.order_by(Post.timestamp.desc()).all()
    page = request.args.get('page',1,type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(page,per_page=5,error_out=False)
    posts = pagination.items
    return render_template('user_info.html',user=user,posts=posts,pagination=pagination)


@user.route('/edit-profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        if current_user.email != form.email.data: #用户更改邮箱时，重新计算头像hash
            new_avatar_hash = hashlib.md5(form.email.data.lower().encode('utf-8')).hexdigest()
            current_user.avatar_hash = new_avatar_hash
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        current_user.password = form.password.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Edit Succeed.')
        return redirect(url_for('user.user_info',username=current_user.name))
    form.name.data = current_user.name
    form.email.data = current_user.email
    form.password.data = current_user.password_hash
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    form.role.data = current_user.role.name
    return render_template('edit_profile.html',form=form)

@user.route('/edit-profile/<int:id>',methods=['GET','POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileForAdminForm(user=user)

    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.password = form.password.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        user.confirmed = form.confirmed.data
        user.role = form.role.data
        db.session.add(user)
        db.session.commit()
        flash('The Profile has been updated.')
        return redirect(url_for('user.user_info',username=user.name))
    
    form.name.data = user.name
    form.email.data = user.email
    form.password.data = user.password_hash
    form.location.data = user.location
    form.about_me.data = user.about_me
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id

    return render_template('edit_profile.html',form=form,user=user)

@user.route('/follow/<username>')
@login_required
@permissions_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(name=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('post.index'))
    if current_user.is_following(user):
        flash('You have already followed this user.')
        return redirect(url_for('user.user_info',username=user.name))

    current_user.follow(user)
    db.session.commit()
    return redirect(url_for('user.user_info',username=user.name))

@user.route('/unfollow/<username>')
@login_required
@permissions_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(name=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('post.index'))
    if not current_user.is_following(user):
        flash("You don't follow this user.")
        return  redirect(url_for('user.user_info',username=user.name))
    current_user.unfollow(user)
    db.session.commit()
    return redirect(url_for('user.user_info',username=user.name))

@user.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(name=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('user.user_info',username=user.name))

    page = request.args.get('page',1,type=int)
    pagination = user.follower.paginate(page,per_page=5,error_out=False)
    followers = [{'user':item.follower,'timestamp':item.timestamp} for item in pagination.items] #item:Follow Instance
    return render_template('follows.html',user=user,
                           title='Followers of',endpoint='user.followers',
                           pagination=pagination,follows=followers
                           )

@user.route('/followed/<username>')
def followed(username):
    user = User.query.filter_by(name=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('user.user_info',username=user.name))

    page = request.args.get('page',1,type=int)
    pagination = user.followed.paginate(page,per_page=5,error_out=False)
    followed = [{'user':item.followed,'timestamp':item.timestamp} for item in pagination.items] #item:Follow Instance
    return render_template('follows.html',user=user,
                           title='Followed by',endpoint='user.followed',
                           pagination=pagination,follows=followed
                           )