<<<<<<< HEAD
import json
import hashlib

=======
import hashlib
>>>>>>> f7784037557ee30ab0439f3eccc32ff7fc9147c5
from flask import session, redirect, url_for, render_template, request
from . import main
from .forms import *
from .users import *
from .functions import *
import json


@main.route('/', methods=['GET', 'POST'])
def index():
    form = UsernameForm()
    if form.validate_on_submit():
        session['username'] = form.username.data
        #session['room'] = form.room.data
        return redirect(url_for('.chat'))
    elif request.method == 'GET':

        form.username.data = session.get('username', '')
    return render_template('index.html', form=form)



@main.route('/passwordCheck', methods=['GET', 'POST'])
def passwordCheck():
    form = PasswordForm()
    if form.validate_on_submit():
<<<<<<< HEAD
        if "challenge" in session.keys() and session['challenge'] == form.challenge.data:
            return redirect(url_for('.chat'))
        else:
            return redirect(url_for('.passwordCheck'))
=======
        if "challenge" in session.keys():
            session['session_key'] = decryptAES(session['challenge'], form.challenge.data).decode()
            room = decryptAES(session['challenge'], form.room.data).decode()
            print(room)
            if int(room) in range(0, 10):
                session['room'] = room
                return redirect(url_for('.chat'))
        return redirect(url_for('.passwordCheck'))
>>>>>>> f7784037557ee30ab0439f3eccc32ff7fc9147c5
    elif request.method == 'GET':
        passwordHash = getUser(session['username'])['passwordHash']
        form.salt = getUser(session['username'])['salt']
        data = hashlib.sha256(bcrypt.gensalt()).hexdigest()[:32]
        session['challenge'] = data
        key = hashlib.sha256(passwordHash.encode()).hexdigest()[:32]
        form.challenge = encryptAES(key, data).decode()
<<<<<<< HEAD
        return render_template('passwordCheck.html', form=form)
=======
>>>>>>> f7784037557ee30ab0439f3eccc32ff7fc9147c5
    return render_template('passwordCheck.html', form=form)


@main.route('/chat')
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
<<<<<<< HEAD
    name = session['username']
    room = session['room']
    print(room)
    if name == '' or room == '':
=======
    username = session.get('username', '')
    room = session.get('room', '')
    if username == '' or room == '':
>>>>>>> f7784037557ee30ab0439f3eccc32ff7fc9147c5
        return redirect(url_for('.index'))
    return render_template('chat.html', username=username, room=room)
