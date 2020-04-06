from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import Required


class UsernameForm(FlaskForm):
    username = StringField('Username', validators=[Required()])
    submit = SubmitField('Send')


class PasswordForm(FlaskForm):
    salt = ""
    challenge = StringField('Challenge', validators=[Required()])
    submit = SubmitField('Send')
