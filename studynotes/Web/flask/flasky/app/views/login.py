from flask import Blueprint,render_template,request,redirect, url_for,flash
auth = Blueprint('auth',__name__)

from flask_login import login_user,logout_user,login_required,current_user
from .forms import LoginForm,RegistrationForm
from app.models import User
from app import db
from app.email import send_email

@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data.strip()=='': #用户名和邮箱二选一
            user = User.query.filter_by(name=form.name.data).first()
        else:
            user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data) #自动在session中标记用户登录状态
            next_url = request.args.get('next') #原url，在访问受保护的页面时跳往登录页，登录后即跳到next_url
            if next_url is None or not next_url.startswith('/'):
                next_url = url_for('post.index')
            return redirect(next_url)
        flash('Invalid username or password.')
    return render_template('login.html',form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user() #删除并重设用户session
    flash('you have been logged out.')
    return redirect(url_for('post.index'))


@auth.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data,
                    email=form.email.data,
                    password=form.password.data
                    )
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(to=user.email,
                   subject='Confirm your account',
                   template='email',
                   user=user,
                   token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('post.index'))
    return render_template('register.html',form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('man.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your accounts.Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('post.index'))

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping() #用户登录后每次发起请求都刷新访问时间
        if not current_user.confirmed \
            and request.blueprint!='auth' \
            and request.endpoint !='static':
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed') 
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('post.index'))
    return render_template('unconfirmed.html')

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(to=current_user.email,
               subject='Confirm your account',
               template='email',
               user=current_user,
               token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('post.index'))
