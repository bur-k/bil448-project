from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio
from .functions import *
import json


@socketio.on('joined', namespace='/chat')
def joined(message): # when a user joined to a room, i.e. socket emits joined, notify all
    room = session.get('room') 
    join_room(room)
    emit('status', {'msg': session.get('username') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message): # when a user sent messages to a room, i.e. socket emits text, first decrypt message with room_key then check hmac if matches notify all
    room = session.get('room')
    new_message = decryptAES(session.get('room_key'), message['msg']).decode()
    json_resp = json.loads(new_message)
    signature = getHmac(session.get('room_key'), json_resp['payload'])
    if signature == json_resp['hmac']:
        emit('message', {'username': session.get('username') + ':', 'msg': message['msg']}, room=room)
    else:
        emit('message', {'username': session.get('username') + ':', 'msg': 'Corrupted message'}, room=room)


@socketio.on('left', namespace='/chat')
def left(message): # when a user left a room, i.e. socket emits left, notify all
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('username') + ' has left the room.'}, room=room)
