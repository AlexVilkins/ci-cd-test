from asyncio import get_event_loop

import grpc
from pyrogram import Client
from grpc_utils.proto import message_pb2_grpc, message_pb2


class ProgressTracker:
    def __init__(self, client: Client = None, bot_name: str = None, static_key: str = None, container_tg=None,
                 container_fast=None):
        self.last_percent = 0
        self.pyro_client: Client = client
        self.bot_name: str = bot_name
        self.static_key: str = static_key
        self.current_id = None
        self.channel_tg = grpc.insecure_channel(f'{container_tg}:50051')
        self.stub_tg = message_pb2_grpc.MessageServiceStub(self.channel_tg)
        self.channel_fast = grpc.insecure_channel(f'{container_fast}:50052')
        self.stub_fast = message_pb2_grpc.MessageServiceStub(self.channel_fast)

    def set_cur_id(self, new_id):
        self.current_id = new_id

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            percent = d['downloaded_bytes'] / d['total_bytes'] * 100 if d['total_bytes'] else 0

            if percent - self.last_percent >= 5:
                percent = round(percent)
                self.stub_tg.SendMessage(message_pb2.Message(text=f"{percent}",
                                                          tg_user_id=str(self.current_id),
                                                          type_mess="progress"))
                self.last_percent = percent

        elif d['status'] == 'finished':
            self.last_percent = 0
