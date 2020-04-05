from flask_wtf import Form
from wtforms.fields import StringField, SubmitField
from wtforms.validators import Required


class UsernameForm(Form):
    username = StringField('Username', validators=[Required()])
    submit = SubmitField('Send')


class PasswordForm(Form):
    passwordHash = ""
    salt = ""
    submit = SubmitField('Send')
