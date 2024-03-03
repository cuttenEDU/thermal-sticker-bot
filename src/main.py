import asyncio
import logging
import sys
import os
from datetime import datetime

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import Message, BufferedInputFile, InputMediaPhoto
from dotenv import load_dotenv

from messages import START_MESSAGE, CANT_PROCESS_ANIMATED, get_random_ready_msg
from image_processing import sticker_to_bw_image
from video_processing import extract_frames

load_dotenv()

TOKEN = os.environ["TG_API_KEY"]
VIDEO_PARTS = eval(os.environ["VIDEO_PARTS"])

dp = Dispatcher()

bot = Bot(TOKEN)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(START_MESSAGE)


@dp.message(F.sticker & F.sticker.is_animated)
async def anim_sticker_handler(message: types.Message) -> None:
    await message.answer(CANT_PROCESS_ANIMATED)


@dp.message(F.sticker & F.sticker.is_video)
async def video_sticker_handler(message: types.Message) -> None:
    file = await bot.get_file(message.sticker.file_id)
    webm_io = await bot.download_file(file.file_path)
    jpegs = extract_frames(webm_io, VIDEO_PARTS)
    jpeg_files = []
    for i, jpeg in enumerate(jpegs):
        input_photo = InputMediaPhoto(media=BufferedInputFile(jpeg,
                                                              f"sticker-bw-{datetime.now().strftime('%d%m%y%H%M%S')}-{i}"))
        if not i:
            input_photo.caption = get_random_ready_msg()
        jpeg_files.append(input_photo)

    await message.answer_media_group(jpeg_files)


@dp.message(F.sticker & ~F.sticker.is_animated & ~F.sticker.is_video)
async def sticker_handler(message: types.Message) -> None:
    file = await bot.get_file(message.sticker.file_id)
    webp_io = await bot.download_file(file.file_path)

    bw_image = sticker_to_bw_image(webp_io, "WEBP")

    bw_image_file = BufferedInputFile(bw_image,
                                      f"sticker-bw-{datetime.now().strftime('%d%m%y%H%M%S')}")

    await message.answer_photo(bw_image_file, caption=get_random_ready_msg())


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
