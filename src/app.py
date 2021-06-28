from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from manager import ConnectionManager
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
                accept_string = "<meta>accept_request</meta>::"
                deny_string = "<meta>deny_request</meta>::"

                if accept_string in data:
                    details = data.split(accept_string)[1].strip()
                    print("details:",details)
                    details = details.split("::")
                    print("details:",details)

                    if len(details) == 2:
                        room_id = details[0]
                        user_id = details[1]
                        print("room_id:",room_id)
                        print("user_id:",user_id)
                        
                        await manager.add_user_to_room(room_id,user_id)
                    else:
                        await manager.send_personal_message(f"Partial Details Found.Please Send Room ID and Member ID",websocket)
                elif deny_string in data:
                    details = data.split(deny_string)[1]
                    details = details.split("::")

                    if len(details) == 2:
                        room_id = details[0]
                        user_id = details[1]
                        user = manager.active_members[user_id]
                        manager.send_personal_message(f"Owner Of The Room {room_id} Has Not Accepted Your Request.",user)
                await manager.broadcast(f"Client says: {data}",room_id)

        except WebSocketDisconnect:

            manager.disconnect(websocket)

            await manager.broadcast(f"Client #{client_id} left the chat",room_id)

@app.websocket("/join_room/{join_details}")
async def join_room(websocket: WebSocket,join_details):
    join_details = json.loads(join_details)
    websocket = await manager.connect(websocket,join_details)
    room_id = join_details['room_id']

    await manager.request_entry(websocket,join_details)
    # if code == status_codes.REQUEST_DENIED:
    #     await manager.send_personal_message("<meta>permission_denied::</meta>Owner Has Denied Your Entry Into The Room.",websocket)
    
    # elif code == status_codes.ROOM_NOT_FOUND:
    #     await manager.send_personal_message("You Room Code Is Expired Or You Have Entered Incorrect Room Code.",websocket)

@app.get('/get_room_details/{room_id:str}')
async def get_room_details(room_id):
    # room_details = manager.room_owners[room_id]
    room_details = {"trial":True}
    print("room_details at the server:",room_details)
    return room_details

# @app.get('/add_to_room/{member_id}')
# async def add_to_room(member_id):
#     manager.find_and_add_to_room(room_id,member_id):