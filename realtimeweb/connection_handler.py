from typing import Any

import websockets


class ConnectionHandler:
    def __init__(self, controller: Any, id: str, websocket: websockets.WebSocketServerProtocol):
        self.controller = controller
        self.id = id
        self.websocket = websocket
        self.queue = None

    # creates task that listens for incoming messages and processes them
    async def listen(self) -> None:
        print('{} opened'.format(self))
        while True:
            try:
                message = await self.websocket.recv()
                await self.handle_message(message)

            except websockets.exceptions.ConnectionClosed as e:
                break

    # push a message to the client
    async def push(self, message: str) -> None:
        await self.websocket.send(message)

    # called in listen(), should be overriden by child class
    def handle_message(self, message: str) -> None:
        pass

    def on_close(self) -> None:
        pass

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __str__(self):
        return 'Conn {}'.format(self.id)
