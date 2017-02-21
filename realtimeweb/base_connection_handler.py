from typing import Any

import websockets


class BaseConnectionHandler:
    """Handles a single connection.

    Public Methods:
        listen()
        push()
        handle_message()
        on_close()
    """

    def __init__(self, controller: Any, id: int, websocket: websockets.WebSocketServerProtocol):
        """Create a ConnectionHandler.

        Arguments:
            controller -- The controller class governing this connection.
            id -- A unique number identifying this connection.
            websocket -- The websocket used for communication with client.
        """

        self.controller = controller
        self.id = id
        self.websocket = websocket

    async def listen(self) -> None:
        """Listen for incoming messages from client."""

        print('{} opened'.format(self))
        while True:
            try:
                message = await self.websocket.recv()
                await self.handle_message(message)

            except websockets.exceptions.ConnectionClosed as e:
                break

    async def push(self, message: str) -> None:
        """Push a message to client."""

        await self.websocket.send(message)

    def handle_message(self, message: str) -> None:
        """Called when a message has been received by client.

        This method is meant to be overriden by subclass.
        """

        pass

    def on_close(self) -> None:
        """Called when the connection is about to be deleted.

        Note that the actual websocket connection is now closed. This method
        is meant to be overriden by subclass.
        """

        pass

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __str__(self):
        return 'Conn {}'.format(self.id)
