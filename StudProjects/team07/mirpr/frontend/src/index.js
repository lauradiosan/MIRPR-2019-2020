// Styles
require('./assets/styles/main.scss');

// Vendor JS is imported as an entry in webpack.config.js

// Elm
var Elm = require('./elm/Main.elm').Elm;
var ws = new WebSocket('ws://0.0.0.0:5000');

var app = Elm.Main.init({});

app.ports.wsMsgSend.subscribe(function(msg){
    ws.send(JSON.stringify({message: msg}));
});

app.ports.wsMsgSendImg.subscribe(function(data){
    var fileId = data[0];
    var message = data[1];

    var reader = new FileReader();
    reader.readAsText($("#" + fileId)[0].files[0]);
    reader.onload = function(e){
        var imgBlob = e.target.result;

        ws.send(JSON.stringify({message, imgBlob}));
    };
});

ws.addEventListener('message', function(event){
    app.ports.wsMsgRecv.send(event.data);
});


