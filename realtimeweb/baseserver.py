import asyncio
from typing import List, Any

import websockets

from realtimeweb.connection_handler import ConnectionHandler


class BaseServer:
    connection_handler = ConnectionHandler

    def __init__(self, HOSTNAME: str, PORT: int):
        self.hostname = HOSTNAME
        self.port = PORT
        self.connections = set()

    def set_connetion_handler_class(self, connection_handler: Any) -> None:
        self.connection_handler = connection_handler

    # start the server and run forever
    def start(self):
        asyncio.get_event_loop().run_until_complete(
            websockets.serve(self.serve, self.hostname, self.port)
        )
        print('Server is listening on port {}...'.format(self.port))
        asyncio.get_event_loop().run_forever()

    # close a connection
    def close(self, conn: ConnectionHandler) -> None:
        print('Closing {}'.format(self))
        conn.on_close()
        del self.connections[conn.id]

    # handle websocket connection requests
    async def serve(self, websocket: websockets.WebSocketServerProtocol, path: str) -> None:
        id = str(websocket)[-9:-1]  # hack - gets mem address, has to be unique
        id = int(id, 16)  # convert hex mem address to int
        connection = self.connection_handler(self, id, websocket)
        self.connections.add(connection)
        await connection.listen()
        self.close(connection)

    # broadcast message out to [connections]
    async def broadcast(self, message: str, connections: List[ConnectionHandler]) -> None:
        for conn in connections:
            await conn.push(message)

    # broadcast message out to all
    async def broadcast_all(self, message: str) -> None:
        for conn in self.connections:
            await conn.push(message)




if __name__ == '__main__':
    server = BaseServer('localhost', 8000)
    server.start()
