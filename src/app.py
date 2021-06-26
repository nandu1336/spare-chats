from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from manager import ConnectionManager
from enum import Enum

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

manager = ConnectionManager()

@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")

    except WebSocketDisconnect:

        manager.disconnect(websocket)

        await manager.broadcast(f"Client #{client_id} left the chat")

import json

@app.websocket("/create_room/{room_details}")
async def create_room(websocket: WebSocket, room_details):
    room_details = json.loads(room_details)
    is_room_created,room_id = await manager.create_room(websocket, room_details)
    print("is_room_created:::",is_room_created,"|| room_id:",room_id)
    if is_room_created:
        # room_id = room_details['room_id']
        try:
            while True:
                await manager.send_personal_message(f"200:{room_id}", websocket)
                data = await websocket.receive_text()
                await manager.broadcast(f"Client #{client_id} says: {data}",room_id)

        except WebSocketDisconnect:

            manager.disconnect(websocket)

            await manager.broadcast(f"Client #{client_id} left the chat",room_id)
