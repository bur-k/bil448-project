import hashlib
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
        is_user_exists, user = getUser(form.username.data)
        if is_user_exists:
            session['username'] = form.username.data
            return redirect(url_for('.passwordCheck'))
    elif request.method == 'GET':
        form.username.data = session.get('username', '')
    return render_template('index.html', form=form)


@main.route('/passwordCheck', methods=['GET', 'POST'])
def passwordCheck():
    form = PasswordForm()
    user = getUser(session['username'])[1]
    if form.validate_on_submit():
        if "challenge" in session.keys():
            response = decryptAES(session['challenge'], form.response.data).decode()
            json_resp = json.loads(response)
            room = int(json_resp['room'])
            session['session_key'] = json_resp['session_key']
            if room in range(0, 10):
                session['room'] = room
                return redirect(url_for('.chat'))
    elif request.method == 'GET' or request.method == 'POST':
        passwordHash = user['passwordHash']
        form.salt = user['salt']
        data = hashlib.sha256(bcrypt.gensalt()).hexdigest()[:32]
        session['challenge'] = data
        key = hashlib.sha256(passwordHash.encode()).hexdigest()[:32]
        form.challenge = encryptAES(key, data).decode()
    return render_template('passwordCheck.html', form=form)


@main.route('/chat')
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    username = session.get('username', '')
    room = session.get('room', '')
    if username == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', username=username, room=room)