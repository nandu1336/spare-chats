from typing import List
from fastapi import FastAPI, WebSocket
import random, string

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.active_rooms: Dict[String,WebSocket] = {}
        self.room_owners: Dict[String,Dict] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        return websocket

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, room_id: str = None):
        if not room_id:
            for connection in self.active_connections:
                await connection.send_text(message)
        else:
            for member in self.active_rooms[room_id]:
                await member.send_text(message)

    async def create_room(self,websocket: WebSocket,room_details):
        print("room_details in manager:",room_details)
        room_id =  "".join(random.choice(string.hexdigits) for _ in range(6))
        # room_id = room_details['room_id']
        print("roomid created::",room_id)
        try: 
            room_members = self.active_rooms[room_id]
            if room_details:
                print("Room ID already used.")
                return False,None
        except KeyError:
            room_members = await self.connect(websocket)
            self.active_rooms[room_id] = [room_members]
            self.room_owners[room_id] = room_details
            return True,room_id