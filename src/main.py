import logging

import PIL
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType
from src.config_parser import get_api_token
from src.image_generator import gen_monet, pil_2_bio
from aiogram.types import InputFile
import io
import src.video_generator
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

API_TOKEN = get_api_token()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Style(StatesGroup):
    start = State()
    monet = State()
    van_gogh = State()


@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message):
    await Style.start.set()
    keyboard_markup = types.ReplyKeyboardMarkup()
    btns_text = ('Monet', 'Van Gogh')
    keyboard_markup.add(*(types.KeyboardButton(text) for text in btns_text))
    await message.reply("Hi!\nI'm NeuronPainterBot!\nPlease, choose painter style:", reply_markup=keyboard_markup)


@dp.message_handler(Text(equals='monet', ignore_case=True), state=Style.start)
async def set_monet_style(message: types.Message, state: FSMContext):
    await Style.monet.set()
    await message.reply('Monet style entered!\nYou can send a photo or videonote now!')


@dp.message_handler(Text(equals='van gogh', ignore_case=True), state=Style.start)
async def set_van_gogh_style(message: types.Message, state: FSMContext):
    await Style.van_gogh.set()
    await message.reply('Van Gogh style entered!\nYou can send a photo or videonote now!')


async def get_img_buf(img):
    file = await bot.get_file(img.file_id)
    file_path = file.file_path
    img_buf = io.BytesIO()
    await bot.download_file(file_path, img_buf)
    img_buf.seek(0)
    return img_buf


@dp.message_handler(content_types=ContentType.PHOTO, state=Style.monet)
async def monet_photo(message: types.Message):
    img_buf = get_img_buf(message.photo[-1])
    img = PIL.Image.open(img_buf)
    out_img = gen_monet(img)
    out_file = InputFile(pil_2_bio(out_img), filename="monet.jpg")
    await message.reply_photo(out_file)


@dp.message_handler(content_types=ContentType.DOCUMENT, state=Style.monet)
async def monet_photo_doc(message: types.Message):
    img_buf = get_img_buf(message.document)
    try:
        img = PIL.Image.open(img_buf)
        out_img = gen_monet(img)
        out_file = InputFile(pil_2_bio(out_img), filename="monet.jpg")
        await message.reply_photo(out_file)
    except IOError:
        await message.reply('Error, not an image, or an unsupported format. Try sending a compressed photo.')


@dp.message_handler(content_types=ContentType.VIDEO_NOTE, state=Style.monet)
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
