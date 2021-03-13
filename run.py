from flask import Flask
from flask_socketio import SocketIO, send, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

socketIo = SocketIO(app, cors_allowed_origins="*")

app.debug = True
app.host = 'localhost'


# @socketIo.on("message")
# def handleMessage(msg):
#     print(msg)
#     send(msg, broadcast=True)
#     return None

users = []


@socketIo.on('connect')
def on_connect():
    retrieve_active_users()


def retrieve_active_users():
    emit('retrieve_active_users', broadcast=True)


@socketIo.on('activate_user')
def on_active_user(data):
    user = data.get('username')
    users.append(user)
    emit('user_activated', {'user': user}, broadcast=True)


@socketIo.on('deactivate_user')
def on_inactive_user(data):
    user = data.get('username')
    emit('user_deactivated', {'user': user}, broadcast=True)


@socketIo.on('join_room')
def on_join(data):
    room = data['room']
    join_room(room)
    emit('open_room', {'room': room}, broadcast=True)


@socketIo.on('leave_chat_app')
def on_leave_chat_app(data):
    print(data)
    username = data['username']
    emit('leave_chat_app', {'username': username}, broadcast=True)


@socketIo.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    print(room, username)
    send(username + ' has left the room.', room=room)


@socketIo.on('send_message')
def on_chat_sent(data):
    room = data['room']
    emit('message_sent', data, room=room)


if __name__ == '__main__':
    socketIo.run(app)
