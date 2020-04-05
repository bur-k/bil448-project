from flask import session, redirect, url_for, render_template, request
from . import main
from .forms import *
from .users import *
import bcrypt


@main.route('/', methods=['GET', 'POST'])
def index():
    form = UsernameForm()
    if form.validate_on_submit():
        session['username'] = form.username.data
        return redirect(url_for('.passwordCheck'))
    elif request.method == 'GET':
        form.username.data = session.get('username', '')
    return render_template('index.html', form=form)


@main.route('/passwordCheck', methods=['GET', 'POST'])
def passwordCheck():
    form = PasswordForm()
    form.passwordHash = getUser(session['username'])['passwordHash']
    form.salt = getUser(session['username'])['salt']
    if form.validate_on_submit():
        if bcrypt.checkpw("pass1", form.responsePasswordHash.encode('utf-8')):
            return form.responsePasswordHash
        else:
            return "no match"
    elif request.method == 'GET':
        return render_template('passwordCheck.html', form=form)
    return render_template('passwordCheck.html', form=form)


@main.route('/chat')
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room=room)
