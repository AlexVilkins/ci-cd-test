import asyncio
import uuid

from fastapi import APIRouter, WebSocket
from starlette.responses import HTMLResponse

from grpc_utils.client import ClientGrpc

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8030/youtube/ws_youtube");
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


router = APIRouter(
    prefix="/youtube",
    tags=["YouTube"]
)
@router.get("/")
async def get():
    return HTMLResponse(html)


@router.websocket("/ws_youtube")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive_text()
    async for response in ClientGrpc().start_stream(url=data, type_mess="sdad"):
        await websocket.send_text(f"Message text was: {response.text}")
    await websocket.close()
