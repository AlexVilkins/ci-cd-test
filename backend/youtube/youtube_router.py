import logging

import grpc
from fastapi import APIRouter, WebSocket, Request
from fastapi.params import Depends
from starlette.responses import HTMLResponse

from grpc_utils.proto import bid_pb2_grpc, bid_pb2
from youtube.schemas import ResponseAddUrl, ConstructURL

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


@router.post("/add_url", response_model=ResponseAddUrl)
async def add_to_query(request: Request, data: ConstructURL = Depends(ConstructURL), ):
    client_host = request.client.host
    channel = grpc.aio.insecure_channel('localhost:50052')
    stub = bid_pb2_grpc.MessageAddServiceStub(channel)
    request = bid_pb2.MessageSendData(user_id=str(client_host),
                                      url=data.url,
                                      type_mess="some_mess")
    response = await stub.SendMessage(request)  # Асинхронный вызов
    position, img_url, description = response.text.split("`")
    return ResponseAddUrl(img_url=img_url, position=position, description=description, user_id=str(client_host))


@router.websocket("/ws_youtube")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive_text()

    # await websocket.send_text(f"Message text was: {response.text}")
    await websocket.close()
