import logging

from fastapi import WebSocket

from utils.Publisher_meta import Observer, SingletonMeta, Subject


class Reporter(Observer):
    def __init__(self, user_id: str, url: str, websocket: WebSocket) -> None:
        self.user_id = user_id
        self.url = url
        self.progress: str = "0"
        self.websocket = websocket

    def __str__(self) -> str:
        return "Reporter"

    async def update(self, subject: Subject) -> None:
        logging.info(f"Reporter: Reacted to the event, get {subject} items")