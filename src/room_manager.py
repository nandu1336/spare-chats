from typing import List
from fastapi import FastAPI, WebSocket
import random, string, json
import status_codes
import select
from connection_manager import manager


class RoomManager:
    def __init__(self):
        self.active_rooms = {}
        self.active_room_codes = ['']

    def create_room(self,room_details,ws):
        ''' 
            room_details = {
                'room_name': 'some name',
                'owner_name': 'Nanda Kishore',
                'owner_id': '6a73913b-b0be-4ea6-9df3-8da7b278a1a2'
            }
        '''

        room_code = self.get_room_code()
        room_details['room_code'] = room_code
        room = Room(room_details,ws)
        self.active_rooms[room_code] = room
        return room
    
    async def join_room(self,join_details,ws):
        room_code = join_details['room_code']
        print("self.active_rooms.keys()::",self.active_rooms.keys())
        print("self.active_rooms[room_code]::",self.active_rooms[room_code])
        try:
            room = self.active_rooms[room_code]
            await room.join_room(join_details,ws)
        except KeyError:
            await ws.send_text("Invalid Room Code.")

    async def add_user_to_room(self,room_code,user_details,ws):
        try:
            room = self.active_rooms[room_code]
            room.add_user_to_room(user_details,ws)
        except KeyError:
            await ws.send_text("Invalid Room Code")        
    
    def get_room_code(self):
        room_code = ''
        while room_code in self.active_room_codes:
            room_code = "".join(random.choice(string.hexdigits) for _ in range(6))
        self.active_room_codes.append(room_code)
        return room_code
    
        
class Room:     
    def __init__(self,room_details,ws):
        self.room_members_sockets = []
        self.room_members_details = {}
        self.room_code = room_details['room_code']
        self.room_name = room_details['room_name']
        self.room_owner = room_details['owner_name']
        self.room_owner_id = room_details['owner_id']
        self.room_owner_ws = ws
        self.room_members_sockets.append(ws)
        self.room_members_details[self.room_owner_id] = {'user_id': self.room_owner_id,'username': self.room_owner}
        
    
    def disconnect(self, websocket: WebSocket):
        self.room_members_sockets.remove(websocket)

    async def send_message_to_owner(self,message):
        print("trying to send_personal_message to owner")
        await self.room_owner_ws.send_text(message)

    async def send_personal_message(self,message: str,ws: WebSocket):
        await ws.send_text(message)

    async def broadcast_message(self,message):
        for member_socket in self.room_members_sockets:
            await member_socket.send_text(message)

    async def join_room(self,member_details,ws):
        print("control inside Room.join_room::",member_details)
        request_string = f"<meta>room_join_request</meta>::{member_details['user_id']}::"
        request_string += f"{member_details['username']} Requested To Join Your Room."

        await self.send_message_to_owner(request_string)

    async def add_user_to_room(self,user_details,ws):
        print("userDetial sin 89:",user_details)
        self.room_members_sockets.append(ws)
        self.room_members_details[user_details['user_id']] = user_details

        await self.broadcast_message(f"{user_details['username']} Has Entered The Chat.")
    
    async def chat(self):
            for member in self.room_members_sockets:
                message = await member.receive_text()
                print("message is not sent by room owner")
                self.broadcast(message)
    
    async def listen_for_joiners(self):
            message = await self.room_owner_ws.receive_text()
            accept_string = "<meta>accept_request</meta>::"
            deny_string = "<meta>deny_request</meta>::"

            if accept_string in message:
                user_id = message.split(accept_string)[1].strip()
                print("user_id:",user_id)
                user = manager.active_members[user_id]
                print("user in 105 :",user)
                if user and user['ws']:
                    await self.add_user_to_room(user,user['ws'])
                else:
                    print(f"user is None:{user is None} || user['ws'] is None:{user['ws'] is None}")
            elif deny_string in message:
                user_id = message.split(deny_string)[1].strip()
            
                user = manager.active_members[user_id]
                manager.send_personal_message(f"Owner Of The Room {room_id} Has Not Accepted Your Request.",user)
                