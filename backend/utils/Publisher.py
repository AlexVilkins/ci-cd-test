import logging

from utils.Reporter import Reporter
from utils.Publisher_meta import Subject, SingletonMeta, Observer
from fastapi import WebSocket


class Publisher(Subject, metaclass=SingletonMeta):

    def __init__(self) -> None:
        self._observers: list[Reporter] = []

    def attach(self, reporter: Reporter) -> None:
        self._observers.append(reporter)
        logging.info(f"Attached an observer. {reporter}")

    def detach(self, reporter: Reporter) -> None:
        self._observers.remove(reporter)

    async def notify(self, user_id: str, url: str) -> None:
        logging.info("Notifying observer...")
        for observer in self._observers:
            """
                Если в обсерверах есть такой элемент (вебсокет также там) то уведомить наблюдателя о том что
                очередь долшла до обьекта с вебсокетом
            """
            if observer.user_id == user_id and observer.url == url:
                await observer.update(self)


    async def start_pooling(self) -> None:
        logging.info("Start pooling")
        while True:
            """
            принимаем все grpc сообщения от работающей очереди pyrogram
            """
            await self.notify()
