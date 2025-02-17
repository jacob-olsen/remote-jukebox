var pageSize = 5
var pageCount = 0
var songCount = 0
var tagetUrl = "/api/songs"

function UpdateSongPage(){
    fetch(tagetUrl + "?page=" + pageCount + "&size=" + pageSize)
    .then(function (response) {
        switch (response.status) {
            // status "OK"
            case 200:
                return response.text();
            // status "Not Found"
            case 404:
                throw response;
        }
    })
    .then(function (mgs) {
        if (typeof mgs == "object") {
            data = mgs
        } else {
            data = JSON.parse(mgs)
        }
        songCount = data["count"]
        list = document.getElementById("songList")
        list.innerHTML = ""

        pageTurn = '<div class="row">'
        pageTurn += '<div class="col">'
        pageTurn += '</div>'
        if (pageCount > 0){
            pageTurn += '<div class="col-1">'
            pageTurn += '<button onclick="pageCount -= 1; UpdateSongPage()">back</button>'
            pageTurn += '</div>'
        }
        pageTurn += '<div class="col-auto">'
        pageTurn += '<p>' + pageCount + '</p>'
        pageTurn += '</div>'
        if (pageCount < Math.ceil(songCount/pageSize)-1){
            pageTurn += '<div class="col-1">'
            pageTurn += '<button onclick="pageCount += 1; UpdateSongPage()">next</button>'
            pageTurn += '</div>'
        }
        pageTurn += '<div class="col">'
        pageTurn += '</div>'
        pageTurn += '</div>'

        list.innerHTML += pageTurn
        
        data["songs"].forEach(element => {
            htmlInfo = '<div class="row" id="' + element["ID"] +'">'
            htmlInfo += '<div class="col">'
            htmlInfo += '<div class="row">'
            htmlInfo += '<div class="col">'
            htmlInfo += '<p id="' + element["ID"] +'name">'+element["name"]+'</p>'
            htmlInfo += '</div>'
            htmlInfo += '<div class="col-auto">'
            htmlInfo += '<button onclick="updateName('+ element["ID"] +', \'' + element["name"] + '\')">edit</button>'
            htmlInfo += '</div>'
            htmlInfo += '</div>'
            htmlInfo += '<div class="row">'
            htmlInfo += '<button onclick="addToList(' + element["ID"] + ')">add to list</button>'
            htmlInfo += '</div>'
            htmlInfo += '</div>'
            htmlInfo += '</div>'
            list.innerHTML += htmlInfo
        });
        
        //document.getElementById("songList").innerHTML = template
    })
    .catch(function (response) {
        // "Not Found"
        console.log(response.statusText);
    });
}