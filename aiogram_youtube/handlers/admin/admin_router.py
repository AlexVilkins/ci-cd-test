import logging
import aiohttp

from aiogram import types, Router, F
from aiogram.filters import CommandStart
import validators
from aiogram.types import BufferedInputFile

from base_settings import base_settings

admin_main_router = Router()
user_bot_id = base_settings.get_user_bot_id()
static_reg = "regxstate"
static_status = "progress"

async def download_thumbnail(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            image_data = await response.read()
            return BufferedInputFile(image_data, filename="thumbnail.jpg")

@admin_main_router.message(CommandStart())
async def user_start(message: types.Message):
    await message.answer("Send URL YouTube video and I send video file after a few minutes")
    logging.info(f"{message.from_user.id} start using")

@admin_main_router.message(F.video)
async def user_start(message: types.Message):
    try:
        if message.video:
            preview, width, height, duration, descr, user_id = message.caption.split(static_reg)
            #thumbnail = await download_thumbnail(preview)
            await message.bot.send_video(chat_id=user_id, video=message.video.file_id,
                                         duration=int(duration),
                                         #thumbnail=thumbnail,
                                         width=int(width),
                                         height=int(height),
                                         supports_streaming=True)
    except Exception as e:
        logging.error(f"{e}")
        await message.answer(text="Error, please send URL YouTube video")

@admin_main_router.message()
async def user_start(message: types.Message):
    if message.chat.id != user_bot_id:
        if validators.url(message.text):
            await message.answer("Link is being processed ...")
            await message.bot.send_message(chat_id=user_bot_id, text=message.text+"`"+str(message.chat.id))
        else:
            await message.answer("URL undefined")
        print("send")

