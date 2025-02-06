var socket = io();
var uiData = {}
var timeSync = 0

//evenst
socket.on('connect', function () {
    console.log("connet to ws server")
    data = socket.emit('hi', { data: 'I\'m connected!' });
    console.log(data)
});

socket.on('message', function (mgs) {
    if (typeof mgs == "object") {
        data = mgs
    } else {
        data = JSON.parse(mgs)
    }

    console.log(data)
    if (data["playing"] != undefined)
        playButon(data["playing"])
    if (data["playList"] != undefined)
        updatePlayList(data["playList"])
    if (data["position"] != undefined)
        updateProgras(data["position"])
    if (data["play_time"] != undefined)
        if (data["length"] != undefined)
            updateTime(data["play_time"],data["length"])
});
//controlse
function play(state) {
    socket.emit("play", { data: state })
}
function addToList(songID) {
    socket.emit("addSongToList", { songID: songID })
}
function rmFromList(songID) {
    socket.emit("rmSongFromList", { songID: songID })
}
function requstPos() {
    socket.emit("playTime", { data: 'I\'m connected!' })
}
function forWard(time){
    socket.emit("forWard", { time: time })
}
function jumpTo(){
    socket.emit("setTime", { time: document.getElementById("posBar").value})
}
//ui Update
function playButon(state) {
    if (uiData["playing"] != state) {
        uiData["playing"] = state
        taget = document.getElementById("playButten")
        if (state) {
            taget.innerHTML = "||"
            timeSync = setInterval(requstPos, 1000)
        } else {
            taget.innerHTML = ">"
            clearInterval(timeSync)
        }
    }
}
function updatePlayList(playList){
    list = document.getElementById("playList")
    list.innerHTML = ""

    playList["list"].forEach(element => {
        htmlInfo = '<div class="row" id="playList' + element["ID"] +'">'
        htmlInfo += '<p>'+element["name"]+'</p>'
        if (element["ID"] == playList["plaingID"]){
            htmlInfo += '<p>plaing</p>'
        }
        htmlInfo += '<button onclick="rmFromList(' + element["ID"] + ')">remove</button>'
        htmlInfo += '</div>'
        list.innerHTML += htmlInfo
    });

    console.log(playList)
}
function updateProgras(pos){
    if (pos < 0){
        pos = 0
    }
    document.getElementById("posText").innerHTML = pos + "%"
    document.getElementById("posBar").value = pos
}
function updateTime(plaing,total){
    if (plaing < 0)
        plaing = 0
    if (total < 0)
        total = 0

    nowSec = Math.floor(plaing / 1000)
    nowMin = Math.floor(nowSec / 60)
    nowSec = nowSec % 60
    if (nowSec < 10)
        nowSec = "0" + nowSec

    totalSec = Math.floor(total / 1000)
    totalMin = Math.floor(totalSec / 60)
    totalSec = totalSec % 60
    if (totalSec < 10)
        totalSec = "0" + totalSec
    document.getElementById("timeText").innerHTML = nowMin + ":" + nowSec + "-" + totalMin + ":" + totalSec
}