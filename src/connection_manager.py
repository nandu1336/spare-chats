from typing import List
from fastapi import FastAPI, WebSocket
import random
import string
import json
import status_codes
import select


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.active_members: Dict = {}

    async def connect(self, websocket: WebSocket, user_details):
        await websocket.accept()
        self.active_connections.append(websocket)
        user_details['ws'] = websocket
        self.active_members[user_details['user_id']] = user_details
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


manager = ConnectionManager()
