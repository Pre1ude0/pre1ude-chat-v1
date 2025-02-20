import flask
from flask import render_template, request, Response
from flask_socketio import SocketIO, emit
from api import get_messages, add_message, start

app = flask.Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='threading')

start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/post/send', methods=['POST'])
def message(): 
    data = request.json
    message = data['message']
    author = data['author']
    if len(message) > 255:
        return 'Message too long', 400
    elif len(author) > 255:
        return 'Username too long', 400
    else:
        add_message(author, message)

        socketio.emit("new_message", {"author": author, "message": message}, room=None, include_self=True)
        return 'Message sent', 200

@app.route('/api/get/msg', methods=['GET'])
def get_msg():
    messages = get_messages()
    return messages, 200

# WebSocket event to notify when a new message arrives
@socketio.on("connect")
def handle_connect():
    print("Client connected")

@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")

def application(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    socketio.run(app, port=3000, host="0.0.0.0")


