from flask import Flask, render_template, request, url_for, redirect
from flask_socketio import SocketIO, send
import json

import service.master

app = Flask(__name__)
socketio = SocketIO(app)
manger = service.master.Manger()

def updateUi(mgs):
    print(mgs)
    
    socketio.send(data=json.dumps(mgs))
manger.addUiUpdateList(updateUi)

@app.route("/")
def hello_world():
    return render_template("index.html")
    

    
#socket
@socketio.on('hi')
def handle_message(data):
    print(data)
    return manger.status()

@socketio.on('playTime')
def handle_message(data):
    socketio.emit("message",manger.playTime())

@socketio.on('play')
def sockePlay(data):
    print(type(data["data"]))
    if data["data"]:
        print("play")
        manger.play()
    else:
        print("pause")
        manger.pause()

@socketio.on('addSongToList')
def addSongToList(data):
    manger.addSongToList(data["songID"])

#api
@app.route("/api/play")
def apiPlay():
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

if __name__=='__main__':
    socketio.run(app)