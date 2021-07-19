from typing import List
from fastapi import FastAPI, WebSocket
import random
import string
import json
from connection_manager import manager
from utilities import MessageType, MessagePurpose, Message
import logging


class RoomManager:
    def __init__(self):
        self.active_rooms = {}
        self.active_room_codes = ['']

    def create_room(self, room_details, ws):
        '''
            room_details = {
                'room_name': 'some name',
                'owner_name': 'Nanda Kishore',
                'owner_id': '6a73913b-b0be-4ea6-9df3-8da7b278a1a2'
            }

            ws: websocket connected to the owner of the room.

            This method takes room_details, creates a room and returns the 6 digit
            alphanumeric code to the owner using which he can invite the people into
            the room.
        '''

        room_code = self.get_room_code()
        room_details['room_code'] = room_code
        room = Room(room_details, ws)
        self.active_rooms[room_code] = room

        return room

    async def join_room(self, join_details, ws):
        '''
            This method takes the user details (join_details parameter) as input,
            finds the room owner for the room the user wants to join and requests
            permission from the owner.
        '''
        room_code = join_details['room_code']
        try:
            room = self.active_rooms[room_code]
            await room.join_room(join_details, ws)
        except KeyError:
            message = Message(room_code, "Invalid Room Code.",
                              "Room Manager", MessagePurpose.OTHERS)
            await ws.send_json(message.as_json())

    async def add_user_to_room(self, room_code, user_details, ws):
        try:
            room = self.active_rooms[room_code]
            room.add_user_to_room(user_details, ws)
        except KeyError:
            await ws.send_text("Invalid Room Code")

    def get_room_code(self):
        room_code = ''
        while room_code in self.active_room_codes:
            room_code = "".join(random.choice(string.hexdigits)
                                for _ in range(6))
        self.active_room_codes.append(room_code)
        return room_code


class Room:
    def __init__(self, room_details, ws):
        self.room_members_sockets = []
        self.room_members_details = {}
        self.room_code = room_details['room_code']
        self.room_name = room_details['room_name']
        self.room_owner = room_details['owner_name']
        self.room_owner_id = room_details['owner_id']
        self.room_owner_ws = ws
        self.room_members_sockets.append(ws)
        self.room_members_details[self.room_owner_id] = {
            'user_id': self.room_owner_id, 'username': self.room_owner}

    async def __broadcast_text_message(self, message, ws=None):
        if ws:
            for member_socket in self.room_members_sockets:
                if member_socket != ws:
                    await member_socket.send_text(message)
        else:
            for member_socket in self.room_members_sockets:
                await member_socket.send_text(message)

    async def __broadcast_json_message(self, message, ws=None):
        if ws:
            for member_socket in self.room_members_sockets:
                if member_socket != ws:
                    await member_socket.send_json(message)
        else:
            for member_socket in self.room_members_sockets:
                await member_socket.send_json(message)

    async def __send_text_message_to_owner(self, message):
        await self.room_owner_ws.send_text(message)

    async def __send_json_message_to_owner(self, message):
        await self.room_owner_ws.send_json(message)

    async def __send_personal_text_message(self, message: str, ws: WebSocket):
        await ws.send_text(message)

    async def __send_personal_json_message(self, message: str, ws: WebSocket):
        await ws.send_json(message)

    def disconnect(self, websocket: WebSocket):
        self.room_members_sockets.remove(websocket)

    async def send_personal_message(self, message: str, ws: WebSocket, message_type=MessageType.JSON_MESSAGE):
        if message_type is MessageType.TEXT_MESSAGE:
            await self.__send_personal_text_message(message, ws)
        else:
            await self.__send_personal_json_message(message, ws)

    async def send_message_to_owner(self, message, message_type=MessageType.JSON_MESSAGE):
        print("trying to send_personal_message to owner")
        if message_type is MessageType.TEXT_MESSAGE:
            await self.__send_text_message_to_owner(message)
        else:
            await self.__send_json_message_to_owner(message)

    async def broadcast_message(self, message, ws=None, message_type=MessageType.JSON_MESSAGE):
        if message_type is MessageType.TEXT_MESSAGE:
            await self.__broadcast_text_message(message, ws=ws)
        else:
            await self.__broadcast_json_message(message, ws=ws)

    async def join_room(self, member_details, ws):
        print("control inside Room.join_room::", member_details)
        request_string = f"<meta>room_join_request</meta>::{member_details['user_id']}::"
        request_string += f"{member_details['username']} Requested To Join Your Room."
        message = Message(self.room_code, request_string,
                          {'user_id': member_details['user_id'], 'username': member_details['username']}, MessagePurpose.JOIN_REQUEST)
        await self.send_message_to_owner(message.as_json())

        while True:
            member_message = await ws.receive_json()
            print("member_message::", member_message)

            await self.broadcast_message(member_message, ws)

    async def add_user_to_room(self, user_details, ws):
        print("userDetial sin 89:", user_details)
        self.room_members_sockets.append(ws)
        self.room_members_details[user_details['user_id']] = user_details

        message = Message(
            self.room_code, "<meta>request_accepted</meta>::200", {}, MessagePurpose.ACCEPT_REQUEST)
        await self.send_personal_message(message.as_json(), ws)

        message = Message(self.room_code, f"{user_details['username']} Has Entered The Chat.", {
        }, MessagePurpose.NEW_MEMBER_JOINED)
        await self.broadcast_message(message.as_json())

    async def listen_for_joiners(self):
        while True:
            response = await self.room_owner_ws.receive_json()
            message = response['content']

            accept_string = "<meta>accept_request</meta>::"
            deny_string = "<meta>deny_request</meta>::"

            if accept_string in message:
                user_id = message.split(accept_string)[1].strip()
                user = manager.active_members[user_id]
                if user and user['ws']:
                    await self.add_user_to_room(user, user['ws'])
                else:
                    print(
                        f"user is None:{user is None} || user['ws'] is None:{user['ws'] is None}")
            elif deny_string in message:
                user_id = message.split(deny_string)[1].strip()

                user = manager.active_members[user_id]
                manager.send_personal_message(
                    f"Owner Of The Room {self.room_name} Has Not Accepted Your Request.", user)
            else:
                await self.broadcast_message(response, self.room_owner_ws)
