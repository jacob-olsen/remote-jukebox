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
