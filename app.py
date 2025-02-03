from flask import Flask, render_template, request, url_for, redirect
from flask_socketio import SocketIO, send

import service.master

app = Flask(__name__)
socketio = SocketIO(app)
manger = service.master.Manger()

def updateUi(mgs):
    print(mgs)
    socketio.send(data=str(mgs))
manger.addUiUpdateList(updateUi)

@app.route("/")
def hello_world():
    return render_template("index.html")
    
@app.route("/api/play")
def play():
    manger.play()
    return "ok"

@app.route("/api/pause")
def pause():
    manger.pause()
    return "ok"

@app.route("/api/skipforward")
def skipForward():
    manger.skip(30000)
    return "ok"

@app.route("/api/skipbackward")
def skipBackward():
    manger.skip(-30000)
    return "ok"

@socketio.on('hi')
def handle_message(data):
    print(data)

if __name__=='__main__':
    socketio.run(app)