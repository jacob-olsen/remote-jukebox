from flask import Flask, render_template, request, url_for, redirect
from flask_socketio import SocketIO, send
from werkzeug.utils import secure_filename
import json
import os

import service.master

app = Flask(__name__)
socketio = SocketIO(app)
manger = service.master.Manger()

UPLOAD_FOLDER = 'temp/upload'
ALLOWED_EXTENSIONS = {"mp3","wav","opus"}

def updateUi(mgs):
    print(mgs)
    
    socketio.send(data=json.dumps(mgs))
manger.addUiUpdateList(updateUi)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/upload", methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect("/")
    
#func
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
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