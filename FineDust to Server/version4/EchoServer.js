#!/usr/bin/env node
var WebSocketServer = require('websocket').server;
var http = require('http');
var Client = [];
var Webos_conn="";
var server = http.createServer(function (request, response) {
    console.log((new Date()) + ' Received request for ' + request.url);
    response.writeHead(404);
    response.end();
});
server.listen(8000, function () {
    console.log((new Date()) + ' Server is listening on port 8080');
});

wsServer = new WebSocketServer({
    httpServer: server,
    // You should not use autoAcceptConnections for production
    // applications, as it defeats all standard cross-origin protection
    // facilities built into the protocol and the browser.  You should
    // *always* verify the connection's origin and decide whether or not
    // to accept it.
    autoAcceptConnections: false
});

function originIsAllowed(origin) {
    // put logic here to detect whether the specified origin is allowed.
    return true;
}


wsServer.on('request', function (request) {
    if (!originIsAllowed(request.origin)) {
        // Make sure we only accept requests from an allowed origin
        request.reject();
        console.log((new Date()) + ' Connection from origin ' + request.origin + ' rejected.');
        return;
    }

    var flag = 0;
    var connection = request.accept(null, request.origin);
    if (connection.remoteAddress == "::ffff:1.39.158.209") {
        Webos_conn = connection;
        console.log("webos 서버 connected");
        //Webos_conn.sendUTF("명훈이 받음?");
    }
    for (i = 0; i < Client.length; i++) {
        if (Client[i].remoteAddress == connection.remoteAddress) {
            flag = 1;
            connection = Client[i];
        }
    }
    if (flag == 0) {
        Client.push(connection);
        connection = Client[Client.length - 1];
    }
    //var connection = request.accept(null, request.origin);
    console.log((new Date()) + ' Connection accepted.');
    connection.on('message', function (message) {
        if (message.type === 'utf8') {
            console.log('Received Message: ' + message.utf8Data + "address : " + connection.remoteAddress);
            console.log("Client 수 :" + Client.length);
            console.log("Client:" + Client);
            //console.log("서버에서 보낸 메시지 : "+"서버(" + connection.remoteAddress + ") :" + message.utf8Data);
            //connection.sendUTF("서버(" + connection.remoteAddress + ") :" + message.utf8Data);
            //Webos_conn.sendUTF("1명훈이 받음?");
            if (Webos_conn!="") {
               // connection.sendUTF("2명훈이 받음?");
               console.log("webos로 전송");
                Webos_conn.sendUTF(message.utf8Data);
            }
            //Webos_conn.sendUTF(message.utf8Data)
        }

        else if (message.type === 'binary') {
            console.log('Received Binary Message of ' + message.binaryData.length + ' bytes');
            connection.sendBytes(message.binaryData);
        }
    });
    connection.on('close', function (reasonCode, description) {
        console.log((new Date()) + ' Peer ' + connection.remoteAddress + ' disconnected.');
    });
});
