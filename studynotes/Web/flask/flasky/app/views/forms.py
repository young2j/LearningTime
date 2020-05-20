from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField, SelectField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo

from app.models import User, Role



#====================================================================================================

class LoginForm(FlaskForm):
    name = StringField('Name', validators=[Length(0, 64)])
    email = StringField('Email',validators=[Length(0,64)])
    password = PasswordField('Password',validators=[DataRequired()])
    remember_me = BooleanField('Keep Logged in')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Length(1,64),Email()])
    name = StringField('Name',validators=[DataRequired(),Length(1,64),
                Regexp('^[A-Za-z][A-Za-z0-9._]*$',0,
                    'Usernames must have only letters,numbers,dots or underscore.')
            ])
    location = StringField('Location',validators=[Length(0,64)])
    password = PasswordField('Password',validators=[DataRequired(),
                EqualTo('password2',message='Passwords must match.')])
    password2 = PasswordField('Comfirm Password',validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self,field): #自定义验证函数 validate+fieldname
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_name(self,field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('Username already in use.')

#====================================================================================================

class EditProfileForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(),Length(0,64)])
    email = StringField('Email', validators=[
                        DataRequired(), Length(1, 64), Email()])
    role = StringField('Role', render_kw={'readonly': True})
    location = StringField('Location',validators=[Length(0,64)])
    about_me = TextAreaField('About me')
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class EditProfileForAdminForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 64),
                                           Regexp('^[A-Za-z][A-Za-z0-9._]*$', 0,
                                                  'Usernames must have only letters,numbers,dots or underscore.')
                                           ])
    email = StringField('Email', validators=[
                        DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    location = StringField('Location',validators=[Length(0,64)])
    about_me = TextAreaField('About me')
    
    role = SelectField('Role',coerce=int,choices='',render_kw={'class':'form-control'},
                        validators=[DataRequired('Pleas choose a role.')])
    confirmed = BooleanField('Confirmed')
    
    submit = SubmitField('Submit')

    def __init__(self, user,*args,**kwargs):
        super(EditProfileForAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id,role.name) for role in Role.query.order_by(Role.name).all()]

        self.user = user
    
    def validate_email(self,field):
        if field.data!=self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
    
    def validate_name(self,field):
        if field.data!=self.user.name and User.query.filter_by(name=field.data).first():
            raise ValidationError('Username already in use.')
#====================================================================================================
class PostForm(FlaskForm):
    # body = TextAreaField("What's on your mind?",validators=[DataRequired()])
    body = PageDownField("What's on your mind?",validators=[DataRequired()])
    submit = SubmitField('Submit')

#====================================================================================================

class CommentForm(FlaskForm):
    body = StringField('Comment:',validators=[DataRequired()])
    submit = SubmitField('Submit')