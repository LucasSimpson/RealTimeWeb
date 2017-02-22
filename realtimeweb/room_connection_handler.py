import json

from realtimeweb import BaseConnectionHandler


class Room(set):
    def __init__(self, id, name=None):
        super().__init__()
        self.name = name
        self.id = id

    def connections(self):
        return list(self)

    def as_json(self):
        """Returns the room as a json string."""

        return json.dumps({
            'id': self.id,
            'name': self.name
        })

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return 'Room#{}'.format(self.id) if not self.name else self.name


class RoomManager:
    """Manages a list of current available rooms."""
    room_id_counter = 0
    rooms = list()

    @staticmethod
    def new_room(name=None) -> int:
        """Creates a new room. Optional name is for asthetics."""

        RoomManager.room_id_counter += 1
        room = Room(RoomManager.room_id_counter, name)
        RoomManager.rooms.append(room)
        return room

    @staticmethod
    def as_json():
        """Return all rooms as json."""

        return json.dumps({'rooms':
                               [json.loads(room.as_json()) for room in RoomManager.rooms]
                           })


class RoomConnectionHandler(BaseConnectionHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room = None

    async def handle_message(self, message: str):
        pass

    async def on_connected(self):
        RoomManager.new_room("LittleFox")
        await self.push(RoomManager.as_json())

    def on_close(self):
        pass

    def broadcast(self, message):
        """Broadcast a message to all clients in the same room"""

        if not self.room:
            raise RuntimeError("broadcast(message) called on a connection that doesn't have a room")
        self.controller.broadcast(message, self.room.connections())
