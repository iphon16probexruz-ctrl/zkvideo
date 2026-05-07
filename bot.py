import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import TOKEN, TEMP_DIR
from handlers.start import router as start_router
from handlers.video import router as video_router

# 📋 Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


# 🧹 Bot ishga tushganda temp papkani tozalash
async def cleanup_temp():
    removed = 0
    for filename in os.listdir(TEMP_DIR):
        filepath = os.path.join(TEMP_DIR, filename)
        try:
            os.remove(filepath)
            removed += 1
        except Exception as e:
            logger.warning(f"O'chirib bo'lmadi: {filepath} | {e}")

    if removed:
        logger.info(f"🧹 Temp papka tozalandi: {removed} ta fayl o'chirildi")
    else:
        logger.info("🧹 Temp papka allaqachon bo'sh")


async def main():
    # 🤖 Bot yaratish
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()

    # 🔌 Routerlarni ulash
    dp.include_router(start_router)
    dp.include_router(video_router)

    # 🧹 Temp tozalash
    await cleanup_temp()

    logger.info("🚀 Bot ishga tushdi!")

    # ▶️ Polling
    await dp.start_polling(bot, skip_updates=True)


if name == "__main__":
    asyncio.run(main())
