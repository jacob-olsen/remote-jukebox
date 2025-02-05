var pageSize = 10
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
        list = document.getElementById("songList")
        list.innerHTML = ""

        data.forEach(element => {
            htmlInfo = '<div class="row" id="' + element["ID"] +'">'
            htmlInfo += '<p>'+element["name"]+'</p>'
            htmlInfo += '<button onclick="addToList(' + element["ID"] + ')">add to list</button>'
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