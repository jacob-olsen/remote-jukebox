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
});
//controlse
function play(state) {
    socket.emit("play", { data: state })
}
function addToList(songID) {
    socket.emit("addSongToList", { songID: songID })
}
function requstPos() {
    socket.emit("playTime", { data: 'I\'m connected!' })
}
function forWard(time){
    socket.emit("forWard", { time: time })
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
        htmlInfo += '<button onclick="addToList(' + element["ID"] + ')">add to list</button>'
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

}