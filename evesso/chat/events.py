from flask import session
from flask.ext.login import current_user
from flask.ext.socketio import emit as _emit, join_room, leave_room
from . import socketio

from evesso import db
from evesso.models import Chatroom, Event


import logging
log = logging.getLogger(__name__)


def character_data():
    return session.get('character', {})


def emit(evt, data, **kwargs):
    _emit(evt, data, **kwargs)
    db.session.add(Event(type=evt, data=data))
    db.session.flush()
    log.info('emit(%r, %r, **%r)', evt, data, kwargs)
    db.session.commit()


@socketio.on('join chatroom', namespace='/chat')
def join_chatroom(room):
    join_room(room)
    evt = dict(room=room)
    evt.update(character_data())
    emit('join chatroom', evt, room=room)


@socketio.on('leave chatroom', namespace='/chat')
def leave_chatroom(room):
    leave_room(room)
    evt = dict(room=room)
    evt.update(character_data())
    emit('leave chatroom', evt, room=room)


@socketio.on('message', namespace='/chat')
def send_message(message):
    message.update(character_data())
    emit('message', message, room=message['room'])
