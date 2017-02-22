/**
 * Created by Lucas on 2017-02-16.
 */




$(function() {

    var chat_rooms = $('#chat-rooms');
    var b_submit = $("#submit");
    var f_message = $("#message");
    var chat_log = $('#chat-log');

    console.log('Working');

    socket = new WebSocket('ws://localhost:8000');

    socket.onopen = function (event) {

        socket.onmessage = function(event) {
            var data = JSON.parse(event.data);
            console.log(data);

            if ("rooms" in data) {
                for (i in data.rooms) {
                    console.log(data.rooms[i]);
                    chat_rooms.append("<button>Join Chat Room #" + data.rooms[i].id + "</button>");
                }
            }

            chat_log.text(chat_log.text() + '  ' + event.data);
        };
    };

    b_submit.click(function() {
        var text = f_message.val();
        f_message.val('');

        console.log('text is ' + text);

        socket.send(text);
    });

});
