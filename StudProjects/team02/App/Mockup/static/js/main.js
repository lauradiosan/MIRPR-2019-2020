var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;
var synced = false;
var requestSet = false;
var spotsTable = [];
var lastNumberFreeSpots = 0;
var lastNumberOccupiedSpots = 0;


function onYouTubeIframeAPIReady() {
    player = new YT.Player('player', {
        height: '334',
        width: '640',
        videoId: 'qwWaQi-Roc4',
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        },
        playerVars: {
            'controls': 0,
            'rel': 0,
            'fs': 0,
            'disablekb': 1,
            'modestbranding': true,
        }
    });
}

function onPlayerReady(event) {
    sendRequest()
    event.target.playVideo();
}

function handleResponse(event) {
    if (event.target.response === "")
        return;

    response = JSON.parse(event.target.response)

    if (!requestSet) {
        requestSet = true;
        setTimeout(sendRequest, response.next_prediction * 1000);
    }
    if (!synced) {
        synced = true;
        player.seekTo(response.elapsed, true);
    }
    setTable(response.spots)
}

function sendRequest() {
    requestSet = false;
    const Http = new XMLHttpRequest();
    const url = 'http://localhost:5000/status';
    Http.open("GET", url)
    Http.send();

    Http.onreadystatechange = handleResponse;
}

function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.PAUSED) {
        player.playVideo();
    }
}

class Spot {
    constructor(_id, occupied, x, y, crop) {
        this.occupied = occupied;
        this.x = x;
        this.y = y;
        this._id = _id;
        this.crop = crop;
    }
}

function setTable(spotsJson) {
    spotsTable = [];

    const spinner = document.getElementById("spinner");
    spinner.removeAttribute('hidden');

    const parkDiv = document.getElementById('parking-table');
    spinner.setAttribute('hidden', '');

    parkDiv.style.display = 'flex';

    // get nr. of frames from db 
    nrFrames = spotsJson.length;

    // extract data into matrix of spots
    posTable = [];
    spotsJson[nrFrames - 1]["spots"].forEach(function(spot) {
        pos = spot['position'];
        x = pos[0];
        y = pos[1];
        if (posTable[x] == undefined) {
            posTable[x] = [];
        }
        newSpot = new Spot(spot['slot_id'], spot['occupied'], x, y, spot['crop']);
        spotsTable.push(newSpot);
        posTable[x][y] = newSpot;
    });

    tableContent = '';
    posTable.forEach(function(row) {
        tableContent += '<tr>';
        row.forEach(function(spot) {
            class_string = (spot.occupied) ? "occupied-spot" : "empty-spot";
            tableContent += '<td><div class="' + class_string + '" onclick="spotShow(this)" id="s' + spot._id + '"></div></td>';
        });
        tableContent += '</tr>';
    })
    document.getElementById('spots-table').innerHTML = tableContent;
    updateCounters();
}

function spotShow(element) {
    spot = spotsTable.filter(spot => ('s' + spot._id) === element.id)[0]
    shownSpot = document.getElementById("highlightspot");
    cover = document.getElementById("cover");
    coverBoundingBox = cover.getClientRects();
    shownSpot.style = "border: 2px solid black";
    shownSpot.style.position = "fixed";
    shownSpot.style.backgroundColor = (spot.occupied) ? "red" : "green";
    shownSpot.style.opacity = 0.3;
    if (spot.x === 2) {
        shownSpot.style.top = Math.round(coverBoundingBox[0].y + spot.crop[1] + 10) + "px";
    }
    else {
        shownSpot.style.top = Math.round(coverBoundingBox[0].y + spot.crop[1] - 10) + "px";
    }
    shownSpot.style.left = Math.round(coverBoundingBox[0].x + spot.crop[0]) + "px";
    shownSpot.style.width = Math.round(spot.crop[2]) + "px";
    shownSpot.style.height = Math.round(spot.crop[3]) + "px";
    shownSpot.style.zIndex = 10;
}

function updateCounters() {
    occupied = spotsTable.filter(spot => spot.occupied).length
    free = spotsTable.filter(spot => !spot.occupied).length

    $('#free-counter')
    .prop('number', lastNumberFreeSpots)
    .animateNumber( {
            number: free
        },
        'normal',
        function() {
            lastNumberFreeSpots = free;
        }
    );

    $('#occupied-counter')
    .prop('number', lastNumberOccupiedSpots)
    .animateNumber( {
            number: occupied
        },
        'normal',
        function() {
            lastNumberOccupiedSpots = occupied;
        }
    );
}