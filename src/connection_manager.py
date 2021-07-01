from typing import List
from fastapi import FastAPI, WebSocket
import random, string, json
import status_codes
import select

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.active_rooms: Dict[String,List[WebSocket]] = {}
        self.room_owners: Dict = {}
        self.active_members: Dict = {}

    async def connect(self, websocket: WebSocket,user_details):
        print("connecet in manager:")
        await websocket.accept()
        # print("awaiting receive_text on member_message")
        self.active_connections.append(websocket)
        user_details['ws'] = websocket
        self.active_members[user_details['user_id']] = user_details
        print("self.active_members.keys()",self.active_members.keys())
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
        
        room_id =  "".join(random.choice(string.hexdigits) for _ in range(6))
        
        try: 
            room_members = self.active_rooms[room_id]
            if room_members:
                print("Room ID already used.")
                return False,None
        except KeyError:
            room_members = await self.connect(websocket,room_details)
            self.active_rooms[room_id] = [room_members]
            room_details['ws'] = websocket
            self.room_owners[room_id] = room_details
            return True,room_id

    async def request_entry(self,websocket,join_details):
        room_id = join_details['room_id']
        print("room join request received for room:",room_id)
        
        try:
            room_members = self.active_rooms[room_id]
            if room_members:
                owner = self.room_owners[room_id]['ws']
                await self.send_personal_message(f"<meta>join_request</meta>::{join_details['user_id']}::{room_id}::{join_details['username']} Wants To Enter Your Room.Allow?",owner)
                
        except KeyError:
            print("no room with the given code found")
            self.send_personal_message("no room with the given code found",websocket)

    async def add_user_to_room(self,room_id,user_id):
        user = self.active_members[user_id]
        user_ws = user['ws']
        self.active_rooms[room_id].append(user_ws)
        
        await self.send_personal_message(f"You Have Joined Room.",user_ws)
        await self.broadcast(f"{user['username']} Has Entered The Room",room_id)
    


manager = ConnectionManager()