import json
import logging
import pickle

import grpc
from fastapi import APIRouter, WebSocket, Request, WebSocketDisconnect
from fastapi.params import Depends
from starlette.responses import HTMLResponse

from grpc_utils.proto import bid_pb2_grpc, bid_pb2
from redis_utils.RedisManager import redis_connection
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
            var ws = new WebSocket("ws://192.168.0.75:8010/youtube/ws_youtube");
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
    response = await stub.SendMessage(request)
    position, img_url, description = response.text.split("`")
    return ResponseAddUrl(img_url=img_url, position=position, description=description, user_id=str(client_host))


@router.websocket("/ws_youtube")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    host = websocket.client.host
    redis_pubsub = redis_connection.redis_client.pubsub()
    logging.info(f"Websocket")
    try:
        await redis_pubsub.subscribe(host)
        async for message in redis_pubsub.listen():
            if message["type"] != 'subscribe':
                data = pickle.loads(message["data"])
                if data["type_mess"] == "video_download":
                    await websocket.send_json(json.dumps(data))
                    break
                if data["type_mess"] == "progress":
                    data["text"] = int(data["text"])
                await websocket.send_json(json.dumps(data))
    except WebSocketDisconnect:
        logging.info("Клиент закрыл соединение")
        await redis_pubsub.unsubscribe(host)
    else:
        await redis_pubsub.unsubscribe(host)
        logging.info("Соединение закрылось самостоятельно")
        await websocket.close()


@router.websocket("/ws_youtube")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    host = websocket.client.host
    print()
    logging.info(host)
    redis_pubsub = redis_connection.redis_client.pubsub()
    logging.info(f"Websocket")
    try:
        await redis_pubsub.subscribe(host)
        async for message in redis_pubsub.listen():
            if message["type"] != 'subscribe':
                data = pickle.loads(message["data"])
                if data["type_mess"] == "video_download":
                    data["text"] = str(data["text"])
                    print(data["text"])
                    await websocket.send_json(json.dumps(data))
                    break
                if data["type_mess"] == "progress":
                    data["text"] = int(data["text"])
                await websocket.send_json(json.dumps(data))
    except WebSocketDisconnect:
        logging.info("Клиент закрыл соединение")
        await redis_pubsub.unsubscribe(host)
    else:
        await redis_pubsub.unsubscribe(host)
        logging.info("Соединение закрылось самостоятельно")
        await websocket.close()
