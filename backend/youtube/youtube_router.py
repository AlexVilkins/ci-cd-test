import json
import logging
import pickle
from urllib.parse import parse_qs

import grpc
from fastapi import APIRouter, WebSocket, Request, WebSocketDisconnect
from fastapi.params import Depends

from grpc_utils.proto import bid_pb2_grpc, bid_pb2
from redis_utils.RedisManager import redis_connection
from youtube.schemas import ResponseAddUrl, ConstructURL

router = APIRouter(
    prefix="/youtube",
    tags=["YouTube"]
)


@router.post("/add_url",
             response_model=ResponseAddUrl,
             summary="Добавить URL видео",
             description="Этот эндпоинт позволяет добавить URL видео YouTube в систему. "
                         "Необходимо предоставить ссылку на видео через query параметр 'url'.")
async def add_to_query(request: Request, data: ConstructURL = Depends(ConstructURL.as_query)):
    address_id = str(request.client.host) + str(request.client.port)
    channel = grpc.aio.insecure_channel('pyrobot:50052')
    stub = bid_pb2_grpc.MessageAddServiceStub(channel)
    request_grpc = bid_pb2.MessageSendData(user_id=address_id,
                                           url=data.url,
                                           type_mess="some_mess")
    response_grpc = await stub.SendMessage(request_grpc)
    position, img_url, description = response_grpc.text.split("`")
    return ResponseAddUrl(img_url=img_url, position=int(position),
                          description=description, user_id=address_id,
                          port=str(request.client.port))


@router.websocket("/ws_youtube/{port}")
async def websocket_endpoint(websocket: WebSocket, port):
    await websocket.accept()
    host = websocket.client.host + str(port)
    redis_pubsub = redis_connection.redis_client.pubsub()
    logging.info(f"Websocket {host}")
    try:
        await redis_pubsub.subscribe(host)
        async for message in redis_pubsub.listen():
            if message["type"] != 'subscribe':
                data = pickle.loads(message["data"])
                if data["type_mess"] == "video_download":
                    await websocket.send_json(data)
                    break
                if data["type_mess"] == "progress" or data["type_mess"] == "queue_position":
                    data["text"] = int(data["text"])
                await websocket.send_json(data)
    except WebSocketDisconnect:
        logging.info("Клиент закрыл соединение")
        await redis_pubsub.unsubscribe(host)
    else:
        await redis_pubsub.unsubscribe(host)
        logging.info("Соединение закрылось самостоятельно")
        await websocket.close()
