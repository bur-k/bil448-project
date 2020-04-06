from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio
from .functions import *
import json


@socketio.on('joined', namespace='/chat')
def joined(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('username') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    new_message = decryptAES(session.get('session_key'), message['msg']).decode()
    json_resp = json.loads(new_message)
    signature = getHmac(session.get('session_key'), json_resp['payload'])
    if signature == json_resp['hmac']:
        emit('message', {'username': session.get('username') + ':', 'msg': message['msg']}, room=room)
    else:
        emit('message', {'username': session.get('username') + ':', 'msg': 'Corrupted message'}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('username') + ' has left the room.'}, room=room)
