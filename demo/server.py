from realtimeweb.baseserver import BaseServer


class DemoServer(BaseServer):
    def new_connection_signal(self, id):
        # TODO send init stuff
        pass

    async def handle_message(self, id, message):
        await self.broadcast_all(message)


def run():
    server = DemoServer('localhost', 8000)
    server.start()
