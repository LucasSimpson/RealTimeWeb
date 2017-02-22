import asyncio
from typing import List, Any

import websockets

from realtimeweb.base_connection_handler import BaseConnectionHandler


class BaseServer:
    """Handles incoming websocket requests and dispatches to ConnectionHandlers.

    Public Methods:
        set_connection_handler_class(connection_handler_class)
        start()
        broadcast(message, connections)
        broadcast_all(message)

    Public Variables:
        connections -- a Set of all current connections
    """

    connection_handler = BaseConnectionHandler

    def __init__(self, HOSTNAME: str, PORT: int):
        """Create a BaseServer set to accept connections from HOSTNAME on port PORT."""

        self.hostname = HOSTNAME
        self.port = PORT
        self.connections = set()

    def set_connetion_handler_class(self, connection_handler_class: Any) -> None:
        """Set the ConnectionHandler class to use."""

        assert issubclass(connection_handler_class, BaseConnectionHandler)
        self.connection_handler = connection_handler_class

    def start(self):
        """Start the server."""

        asyncio.get_event_loop().run_until_complete(
            websockets.serve(self._serve, self.hostname, self.port)
        )
        print('Server is listening on port {}...'.format(self.port))
        asyncio.get_event_loop().run_forever()

    def _close(self, connection: BaseConnectionHandler) -> None:
        """Close a given connection."""

        print('Closing {}'.format(connection))
        connection.on_close()
        self.connections = self.connections - set([connection])
        # del self.connections[connection.id]

    async def _serve(self, websocket: websockets.WebSocketServerProtocol, path: str) -> None:
        """Serve a given websocket."""

        id = str(websocket)[-9:-1]  # hack - gets mem address, has to be unique
        id = int(id, 16)  # convert hex mem address to int
        connection = self.connection_handler(self, id, websocket)
        self.connections.add(connection)
        await connection.listen()
        self._close(connection)

    async def broadcast(self, message: str, connections: List[BaseConnectionHandler]) -> None:
        """Send message to all [connections]."""

        for conn in connections:
            await conn.push(message)

    async def broadcast_all(self, message: str) -> None:
        """Send message to all connections."""
        for conn in self.connections:
            await conn.push(message)
