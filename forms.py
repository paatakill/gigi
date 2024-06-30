from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, DateField, RadioField, SelectField, SubmitField, IntegerField, StringField, TextAreaField
from wtforms.validators import DataRequired, length, equal_to
from flask_wtf.file import FileField, FileAllowed, FileSize

class RegisterForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired(), length(min=6, max=64)])
    repeat_password = PasswordField(validators=[DataRequired(), equal_to("password", message="Passwords don't match")])
    phonenum = IntegerField(validators=[DataRequired()])
    date = DateField()
    role = RadioField("choose role", choices=['Student', 'Teacher'], validators=[DataRequired()])

    submit = SubmitField("Register")

class AuthorizationForm(FlaskForm):
    username = StringField()
    password = PasswordField()

    login = SubmitField("Authorization")


class ReviewForm(FlaskForm):
    user = StringField('User')
    role = StringField('Role')
    title = StringField('Title', validators=[DataRequired(), length(min=1, max=100)])
    content = TextAreaField('Content', validators=[DataRequired()])
    image = FileField('image', 
                      validators=[FileAllowed(['jpg', 'png'], message='Images only!')
                                  ,FileSize(1024 * 1024 * 16)])
    
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    user = StringField('User')
    role = StringField('Role')
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post Comment')

class EmailForm(FlaskForm):
    id = IntegerField()
    user = StringField('User')
    email = StringField("please enter your Email")
    submit = SubmitField("Send")