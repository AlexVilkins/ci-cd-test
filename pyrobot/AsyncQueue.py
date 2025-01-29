import asyncio
import os
import uuid
from asyncio import Queue

import yt_dlp.utils

from base_settings import base_settings
from grpc_utils.proto import message_pb2
from grpc_utils.proto_ws import ws_pb2


class AsyncQueue:
    def __init__(self, stub_tg=None, stub_fast=None, progress_tracker=None, static_ydl=None):
        self.queue = Queue()
        self.stub_tg = stub_tg
        self.stub_fast = stub_fast
        self.progress_tracker = progress_tracker
        self.static_ydl = static_ydl
        self.static_status = base_settings.get_status()
        self.static_reg = base_settings.get_reg()
        self.bot_name = base_settings.get_bot_name()

    async def add_to_queue_from_browser(self, url=None, user_id=None):
        check_result = await self.check_video_from_browser(url=url)
        if isinstance(check_result, tuple):
            url_img, description = check_result
            position = self.queue.qsize() + 1
            await self.queue.put((None, url, user_id))
            print(f"Item added to queue")
            return position, url_img, description
        return check_result

    async def add_to_queue(self, client=None, message=None):
        url, chat = message.text.split("`")
        if await self.check_video(chat=chat, url=url):
            position = self.queue.qsize() + 1
            if client:
                self.stub_tg.SendMessage(message_pb2.Message(text=f"Queue position: {position}",
                                                             tg_user_id=chat,
                                                             type_mess="position"))
            await self.queue.put((client, url, chat))
            print(f"Item added to queue")

    async def worker(self):
        print("worker start")
        while True:
            if not self.queue.empty():
                item = self.queue._queue[0]
                await self.work(item)
                await self.queue.get()
                self.queue.task_done()
                await self.send_change_queue_status()
            await asyncio.sleep(1)

    async def send_change_queue_status(self):
        for position, element in enumerate(list(self.queue._queue)):
            self.stub_fast.SendMessage(ws_pb2.MessageSendPyro(user_id=element[2],
                                                              text=f"{position + 1}",
                                                              type_mess="queue_position"))



    async def work(self, item):
        client, url, chat = item
        if client:
            await self.tg_work(*item)
        else:
            await self.browser_work(*item)

    async def browser_work(self, client, url, chat):
        print(f"Start working browser on {chat}")

        self.progress_tracker.set_cur_id(chat)
        try:
            with self.static_ydl as ydl:
                info = ydl.extract_info(url, download=False)
                file_path = ydl.prepare_filename(info)
                video_duration = info.get('duration', None)
                img_url = info.get('thumbnail')
                description = info.get('title')
                self.stub_fast.SendMessage(ws_pb2.MessageSendPyro(user_id=chat,
                                                                  text=f"{img_url}`{description}",
                                                                  type_mess="video_info"))
                ydl.download(url)
        except Exception as e:
            print(e)
            self.stub_fast.SendMessage(ws_pb2.MessageSendPyro(user_id=chat,
                                                              text="Loading error",
                                                              type_mess="error_load"))
            return
        try:
            with open(file_path, "rb") as _:
                pass
        except FileNotFoundError:
            self.stub_fast.SendMessage(ws_pb2.MessageSendPyro(user_id=chat,
                                                              text=f"Sever side error\n",
                                                              type_mess="error_server"))
            return
        self.stub_fast.SendMessage(ws_pb2.MessageSendPyro(user_id=chat,
                                                          text=f"{file_path}",
                                                          type_mess="video_download"))
        os.remove(file_path)
        print(f"End working on {chat}")

    async def tg_work(self, client, url, chat):
        print(f"Start working tg on chat{chat}")
        self.progress_tracker.set_cur_id(chat)
        try:
            with self.static_ydl as ydl:
                info = ydl.extract_info(url, download=False)
                file_path = ydl.prepare_filename(info)
                video_duration = info.get('duration', None)
                img_url = info.get('thumbnail')
                description = info.get('title')
                self.stub_tg.SendMessage(message_pb2.Message(text=f"{url}`{img_url}`{description}",
                                                             tg_user_id=chat,
                                                             type_mess="url"))
                ydl.download(url)
        except:
            try:
                ydl.download(url)
            except:
                self.stub_tg.SendMessage(message_pb2.Message(text=f"Loading error",
                                                             tg_user_id=chat,
                                                             type_mess="error_load"))
                return
            return
        try:
            with open(file_path, "rb") as _:
                pass
        except FileNotFoundError:
            self.stub_tg.SendMessage(message_pb2.Message(text=f"Sever side error\n"
                                                              f"Please try later",
                                                         tg_user_id=chat,
                                                         type_mess="error_server"))
            return
        self.stub_tg.SendMessage(message_pb2.Message(text=f"{video_duration}",
                                                     tg_user_id=chat,
                                                     type_mess="send_video"))
        await client.send_video(chat_id=self.bot_name, video=file_path,
                                caption=f"Вот ваше видео!{self.static_reg}{chat}")
        self.stub_tg.SendMessage(message_pb2.Message(text=f"{video_duration}",
                                                     tg_user_id=chat,
                                                     type_mess="video_delivered"))
        os.remove(file_path)
        print(f"End working on {chat}")

    async def check_video(self, chat, url):
        try:
            with self.static_ydl as ydl:
                info = ydl.extract_info(url, download=False)
                video_duration = info.get('duration', None)
        except yt_dlp.utils.DownloadError as error:
            if "Unsupported URL" in error.msg:
                self.stub_tg.SendMessage(message_pb2.Message(text=f"{error.msg}\n",
                                                          tg_user_id=chat,
                                                          type_mess="repeat"))
                return
            self.stub_tg.SendMessage(message_pb2.Message(text=f"Video quality is too low for 720p upload\n",
                                                      tg_user_id=chat,
                                                      type_mess="repeat"))
            return
        if video_duration > 3599:
            self.stub_tg.SendMessage(
                message_pb2.Message(text=f"We are currently not loading videos for more than an hour\n",
                                    tg_user_id=chat,
                                    type_mess="repeat"))
            return
        for item in self.queue._queue:
            if item[2] == chat:
                self.stub_tg.SendMessage(message_pb2.Message(text=f"One of your videos is already in the queue\n"
                                                               f"Please wait for loading",
                                                          tg_user_id=chat,
                                                          type_mess="repeat"))
                return
        return True

    async def check_video_from_browser(self, url):
        try:
            with self.static_ydl as ydl:
                info = ydl.extract_info(url, download=False)
                video_duration = info.get('duration', None)
                description = info.get('title')
                img_url = info.get('thumbnail')
        except yt_dlp.utils.DownloadError as error:
            if "Unsupported URL" in error.msg:
                return error.msg
            return "Video quality is too low for 720p upload"
        if video_duration > 3599:
            return "We are currently not loading videos for more than an hour"
        # for item in self.queue._queue:
        #     if item[2] == chat:
        #         self.stub.SendMessage(message_pb2.Message(text=f"One of your videos is already in the queue\n"
        #                                                        f"Please wait for loading",
        #                                                   tg_user_id=chat,
        #                                                   type_mess="repeat"))
        #         return "We are currently not loading videos for more than an hour"
        return img_url, description
