from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):     #catching the field name that is going to be validated by passing the field name as an argument
        
        query = User.query.filter_by(email=email.data).first() 
        if query:                       
            raise ValidationError('Email is already taken.')



    def validate_username(self, username):     
        
        query = User.query.filter_by(username=username.data).first() 
        if query:                       
            raise ValidationError('Username is already taken.') 


class LoginForm(FlaskForm):
    username = StringField('username',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')




class UpdateForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'gif'])])
    
    submit = SubmitField('Update')





    def validate_username(self, username):      #catching the field name that is going to be validated by passing the field name as an argument
        if username.data != current_user.username:
            query = User.query.filter_by(username=username.data).first() 
            if query:                       
                raise ValidationError('Username is already taken.') 


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

