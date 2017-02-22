from realtimeweb import BaseServer
from realtimeweb.room_connection_handler import RoomConnectionHandler


class DemoConnectionHandler(RoomConnectionHandler):
    async def handle_message(self, message: str) -> None:
        await self.controller.broadcast_all(message)


def run():
    server = BaseServer('localhost', 8000)
    server.set_connetion_handler_class(DemoConnectionHandler)
    server.start()
