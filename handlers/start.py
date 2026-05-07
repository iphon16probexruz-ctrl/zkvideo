import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.reply import main_menu

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def start_handler(message: Message):
    logger.info(f"Yangi foydalanuvchi: {message.from_user.id}")

    await message.answer(
        "Assalomu alaykum! 👋\n\n"
        "🎬 Videoga <b>DVD-style</b> logo qo'yish uchun\n"
        "quyidagi tugmani bosing 👇",
        reply_markup=main_menu(),
    )
