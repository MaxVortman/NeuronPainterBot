import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType
from src.config_parser import get_api_token
from src.image_generator import gen_monet
from aiogram.types import InputFile
import io

API_TOKEN = get_api_token()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm NeuronPainterBot!\nPowered by aiogram.")


@dp.message_handler(content_types=ContentType.PHOTO)
async def monet_photo(message: types.Message):
    photo = message.photo[2]
    file = await bot.get_file(photo.file_id)
    file_path = file.file_path
    img_buf = io.BytesIO()
    await bot.download_file(file_path, img_buf)
    img_buf.seek(0)
    out_img = gen_monet(img_buf)
    out_file = InputFile(out_img, filename="monet.jpg")
    await message.reply_photo(out_file)


@dp.message_handler(content_types=ContentType.VIDEO_NOTE)
async def video_note_echo(message: types.Message):
    file = await bot.get_file(message.video_note.file_id)
    file_path = file.file_path
    await bot.download_file(file_path, "test.mp4")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)