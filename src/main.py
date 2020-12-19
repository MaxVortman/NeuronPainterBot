import logging

import PIL
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType
from src.config_parser import get_api_token
from src.image_generator import gen_monet, pil_2_bio
from aiogram.types import InputFile
import io
import src.video_generator

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
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    file_path = file.file_path
    img_buf = io.BytesIO()
    await bot.download_file(file_path, img_buf)
    img_buf.seek(0)
    img = PIL.Image.open(img_buf)
    out_img = gen_monet(img)
    out_file = InputFile(pil_2_bio(out_img), filename="monet.jpg")
    await message.reply_photo(out_file)


@dp.message_handler(content_types=ContentType.DOCUMENT)
async def monet_photo_doc(message: types.Message):
    file = await bot.get_file(message.document.file_id)
    file_path = file.file_path
    img_buf = io.BytesIO()
    await bot.download_file(file_path, img_buf)
    img_buf.seek(0)
    try:
        img = PIL.Image.open(img_buf)
        out_img = gen_monet(img)
        out_file = InputFile(pil_2_bio(out_img), filename="monet.jpg")
        await message.reply_photo(out_file)
    except IOError:
        await message.reply('Error, not an image, or an unsupported format. Try sending a compressed photo.')


@dp.message_handler(content_types=ContentType.VIDEO_NOTE)
async def video_note_monet(message: types.Message):
    file = await bot.get_file(message.video_note.file_id)
    file_path = file.file_path
    video_path = '../data/input.mp4'
    await bot.download_file(file_path, video_path)
    src.video_generator.gen_monet(video_path)
    out_file = InputFile('../data/output.mp4', filename="monet.mp4")
    await message.reply_video_note(out_file)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)