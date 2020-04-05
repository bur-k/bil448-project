from base64 import b64encode
import json

from Crypto.Cipher import AES
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
    passwordHash = getUser(session['username'])['passwordHash']
    form.salt = getUser(session['username'])['salt']

    data = bcrypt.gensalt()
    print(data)
    key = passwordHash[:16]
    cipher = AES.new(key, AES.MODE_CTR)
    ct_bytes = cipher.encrypt(data)
    nonce = b64encode(cipher.nonce).hex()
    ct = b64encode(ct_bytes).hex()
    form.challenge = json.dumps({'nonce': nonce, 'ciphertext': ct})
    print(form.challenge)

    if form.validate_on_submit():
        print("")
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
