from flask import session, redirect, url_for, render_template, request, jsonify
from . import main
from .forms import *
from .users import *
from .functions import *
import json


@main.route('/', methods=['GET', 'POST'])
def index(): # index page, the displayed page when localhost:5000/ loaded
    form = UsernameForm()
    if form.validate_on_submit(): # checks form data
        is_user_exists, user = getUser(form.username.data)
        if is_user_exists:
            session['username'] = form.username.data
            return redirect(url_for('.passwordCheck')) # if username has a match redirect to passwordCheck page
    elif request.method == 'GET':
        form.username.data = session.get('username', '')
    return render_template('index.html', form=form)


@main.route('/passwordCheck', methods=['GET', 'POST'])
def passwordCheck(): # 
    form = PasswordForm()
    user = getUser(session['username'])[1] # get user with given username
    if form.validate_on_submit():
        if "challenge" in session.keys(): # if challenge exists in session
            response = decryptAES(session['challenge'], form.response.data).decode() # dexrypt it
            json_resp = json.loads(response)
            room = int(json_resp['room'])
            session['session_key'] = json_resp['session_key']
            if room in range(0, 10): # if room value from loaded json that client sent is between 0-10, otherwise it means client could not pass challenge response
                session['room'] = room
                return redirect(url_for('.chat')) # redirect it to chat page
    elif request.method == 'GET' or request.method == 'POST':
        passwordHash = user['passwordHash']
        form.salt = user['salt']
        data = hashlib.sha256(bcrypt.gensalt()).hexdigest()[:64] # create challenge
        session['challenge'] = data
        key = hashlib.sha256(passwordHash.encode()).hexdigest()[:64]
        form.challenge = encryptAES(key, data).decode() # encrypt challenge with hash of user password
    return render_template('passwordCheck.html', form=form)


@main.route('/chat')
def chat():
    username = session.get('username', '')
    room = getRoom(session.get('room', ''))
    session['room_key'] = room["room_key"]
    room = encryptAES(session['session_key'], room['room_key']).decode()

    if username == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', username=username, room=room)
