import asyncio
import threading

import yt_dlp
from pyrogram import Client, filters

from AsyncQueue import AsyncQueue
from base_settings import base_settings
from utils import ProgressTracker

API_ID = base_settings.get_id()
API_HASH = base_settings.get_hash()
bot_name = base_settings.get_bot_name()
pwd = base_settings.get_pwd()
static_status = base_settings.get_status()
static_reg = base_settings.get_reg()
container_tg = base_settings.get_tg_container()
container_fast = base_settings.get_fast_container()
ydl_opts = base_settings.get_yt_dlp_options()


app = Client("teletoon_userbot", api_id=API_ID, api_hash=API_HASH)


progress_tracker = ProgressTracker(client=app, bot_name=bot_name,
                                   static_key=static_status + static_reg,
                                   container_tg=container_tg,
                                   container_fast=container_fast)
ydl_opts['progress_hooks'].append(progress_tracker.progress_hook)

static_ydl = yt_dlp.YoutubeDL(ydl_opts)
queue = AsyncQueue(stub=progress_tracker.stub_tg, static_ydl=static_ydl, progress_tracker=progress_tracker)


def dome():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(start_worker_and_grpc())


async def start_worker_and_grpc():
    await asyncio.gather(start_worker(),
                         start_grpc())


async def start_worker():
    await queue.worker()


async def start_grpc():
    pass


@app.on_message(filters.chat(bot_name))
async def reply_with_video(client, message):
    print("get message")
    await queue.add_to_queue(client, message)


thread = threading.Thread(target=dome)
thread.start()
app.run()