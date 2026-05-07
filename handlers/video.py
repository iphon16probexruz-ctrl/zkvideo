import asyncio
import gc
import logging
import os
import uuid

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message

from config import TEMP_DIR
from keyboards.reply import back_menu, main_menu
from services.ffmpeg_service import apply_watermark
from states import VideoState

router = Router()
logger = logging.getLogger(__name__)


# ─── Tugma bosildi ──────────────────────────────────────────
@router.message(F.text == "🎬 Videoga logo qo'yish")
async def ask_video(message: Message, state: FSMContext):
    await state.set_state(VideoState.waiting_for_video)

    await message.answer(
        "📤 Videoni yuboring\n"
        "<i>(video yoki fayl ko'rinishida)</i>",
        reply_markup=back_menu(),
    )


# ─── Orqaga ─────────────────────────────────────────────────
@router.message(VideoState.waiting_for_video, F.text == "🔙 Orqaga")
async def go_back(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        "⬅️ Asosiy menyuga qaytdingiz",
        reply_markup=main_menu(),
    )


# ─── Video qabul ────────────────────────────────────────────
@router.message(VideoState.waiting_for_video)
async def handle_video(message: Message, state: FSMContext):
    # Faqat video yoki document qabul qilamiz
    if not message.video and not message.document:
        await message.answer("❌ Iltimos, video yuboring")
        return

    processing_msg = await message.answer("⏳ Video qayta ishlanmoqda...")

    uid = str(uuid.uuid4())
    input_path = os.path.join(TEMP_DIR, f"{uid}_input.mp4")
    output_path = os.path.join(TEMP_DIR, f"{uid}_output.mp4")

    success = False

    try:
        # ─── Faylni yuklab olish ─────────────────────────────
        if message.video:
            file_id = message.video.file_id
        else:
            file_id = message.document.file_id

        file = await message.bot.get_file(file_id)
        await message.bot.download_file(file.file_path, input_path)

        logger.info(f"Video yuklandi: {uid}")

        # ─── Watermark qo'yish (async) ───────────────────────
        await apply_watermark(input_path, output_path)

        # ─── Natijani yuborish ───────────────────────────────
        output_file = FSInputFile(output_path)

        if message.video:
            await message.answer_video(output_file)
        else:
            await message.answer_document(output_file)

        success = True
        logger.info(f"Video yuborildi: {uid}")

    except Exception as e:
        logger.error(f"Xatolik [{uid}]: {e}")

        await message.answer(
            f"❌ Xatolik yuz berdi:\n<code>{e}</code>"
        )

    finally:
        # ─── Temp fayllarni tozalash ─────────────────────────
        gc.collect()
        await asyncio.sleep(0.5)

        for path in (input_path, output_path):
            if os.path.exists(path):
                try:
                    os.remove(path)
                except Exception as err:
                    logger.warning(f"O'chirib bo'lmadi: {path} | {err}")

        await state.clear()

        # ─── Yakuniy xabar ───────────────────────────────────
        if success:
            await processing_msg.edit_text("✅ Tayyor!")
            await message.answer(
                "🎉 Video muvaffaqiyatli tayyorlandi!",
                reply_markup=main_menu(),
            )
        else:
            await processing_msg.edit_text("❌ Video qayta ishlanmadi")
            await message.answer(
                "Qaytadan urinib ko'ring 👇",
                reply_markup=main_menu(),
            )
            await state.clear()
