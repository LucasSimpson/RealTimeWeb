import asyncio

import websockets


class BaseServer:
    def __init__(self, HOSTNAME, PORT):
        self.hostname = HOSTNAME
        self.port = PORT
        self.ids = list()
        self.websockets = {}
        self.queues = {}

    # start the server and run forever
    def start(self):
        asyncio.get_event_loop().run_until_complete(
            websockets.serve(self.serve, self.hostname, self.port)
        )
        print('Server is listening on port {}...'.format(self.port))
        asyncio.get_event_loop().run_forever()

    # handle websocket connection requests
    async def serve(self, websocket, path):
        # get id
        id_ = str(websocket)[-9:-1]  # hack. gets mem address, has to be unique
        print('new connection for {}'.format(id_))
        self.new_connection_signal(id_)

        # track id and new websocket, queue
        self.ids.append(id_)
        self.websockets[id_] = websocket
        self.queues[id_] = asyncio.Queue()

        # create listening task
        async def conn_listen():
            while True:
                try:
                    message = await websocket.recv()
                    await self.handle_message(id_, message)

                except websockets.exceptions.ConnectionClosed as e:
                    print('Closing {}'.format(id_))
                    self.connection_dropped_signal(id_)
                    del self.websockets[id_]
                    del self.queues[id_]
                    del self.ids[self.ids.index(id_)]
                    break
        asyncio.get_event_loop().create_task(conn_listen())

        # dopushing task
        while id_ in self.queues:
            item = await self.queues[id_].get()
            await websocket.send(item)

    # broadcast message out to all [ids]
    async def broadcast(self, message, ids):
        for id in ids:
            await self.queues[id].put(message)

    # broadcast message out to all
    async def broadcast_all(self, message):
        for id in self.ids:
            await self.queues[id].put(message)

    # boardcasts message to all except id
    async def broadcast_all_except(self, id_, message):
        for id in self.ids:
            if not id == id_:
                await self.queues[id].put(message)

    # push message to a specific id
    async def push_to(self, message, id):
        await self.queues[id].put(message)

    # called when there is any new connection
    def new_connection_signal(self, id):
        pass

    # called when a connection is deleted
    def connection_dropped_signal(self, id):
        pass

    # called when message is received from client
    def handle_message(self, id, message):
        pass


if __name__ == '__main__':
    server = BaseServer('localhost', 8000)
    server.start()
