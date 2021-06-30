from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from connection_manager import manager
from room_manager import Room, RoomManager
from fastapi.middleware.cors import CORSMiddleware
import status_codes

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"]
)

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



room_manager = RoomManager()

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
active_rooms = {}

@app.websocket("/create_room/{room_details}")
async def create_room(websocket: WebSocket, room_details):
    await websocket.accept()
    room_details = json.loads(room_details)
    room = room_manager.create_room(room_details,websocket)
    room_code = room.room_code
    print("room_created || room_code:",room_code)
    
    await websocket.send_text(f"200:{room_code}")
    while True:
        try:
            await room.listen_for_joiners()
            await room.chat()
            

        except WebSocketDisconnect:

            room.disconnect(websocket)
            await room.broadcast_message(f"Client left the chat")
            print(f"Client left the chat")

@app.websocket("/join_room/{join_details}")
async def join_room(websocket: WebSocket,join_details):
    join_details = json.loads(join_details)
    websocket = await manager.connect(websocket,join_details)
    room_code = join_details['room_code']

    await room_manager.join_room(join_details,websocket)  

@app.get('/get_room_details/{room_code:str}')
async def get_room_details(room_code):
    # room_details = manager.room_owners[room_code]
    room_details = {"trial":True}
    print("room_details at the server:",room_details)
    return room_details

# @app.get('/add_to_room/{member_id}')
# async def add_to_room(member_id):
#     manager.find_and_add_to_room(room_code,member_id):
