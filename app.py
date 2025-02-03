from flask import Flask, render_template, request, url_for, redirect

import service.master

app = Flask(__name__)
manger = service.master.Manger()

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


if __name__=='__main__':
    app.run(debug=True)