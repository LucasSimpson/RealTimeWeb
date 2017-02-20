/**
 * Created by Lucas on 2017-02-16.
 */

$(function() {

    console.log('Working');

    socket = new WebSocket('ws://localhost:8000');

    socket.onopen = function (event) {


        socket.onmessage = function(event) {
            console.log(event);

            var dom = $("#chatlog");

            dom.text(dom.text() + '  ' + event.data);
        };
    };

    $("#submit").click(function() {
        var text = $("#message").val();
        $("#message").val('');

        console.log('text is ' + text);

        socket.send(text);
    });

});
