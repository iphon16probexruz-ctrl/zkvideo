import asyncio
import logging
import os
import shutil

from config import LOGO_PATH, CRF, PRESET, VX, VY

logger = logging.getLogger(__name__)


async def apply_watermark(input_path: str, output_path: str) -> None:

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input video topilmadi: {input_path}")

    if not os.path.exists(LOGO_PATH):
        raise FileNotFoundError(f"Logo topilmadi: {LOGO_PATH}")

    # Railway/Linux ffmpeg detect
    ffmpeg = shutil.which("ffmpeg")

    if not ffmpeg:
        raise RuntimeError("FFmpeg serverda topilmadi!")

    logger.info(f"FFmpeg topildi: {ffmpeg}")

    filter_expr = (
        f"[1:v]format=rgba,"
        f"scale='min(iw,ih)*1.2':-1[logo];"
        f"[0:v][logo]overlay="
        f"x='abs(mod(n*{VX},2*(W-w))-(W-w))':"
        f"y='abs(mod(n*{VY},2*(H-h))-(H-h))'"
    )

    command = [
        ffmpeg,
        "-y",
        "-hide_banner",
        "-loglevel", "error",
        "-i", input_path,
        "-i", LOGO_PATH,
        "-filter_complex", filter_expr,
        "-c:v", "libx264",
        "-preset", PRESET,
        "-crf", str(CRF),
        "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        "-threads", "0",
        output_path,
    ]

    logger.info(f"FFmpeg ishga tushdi: {os.path.basename(input_path)}")

    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    _, stderr = await process.communicate()

    if process.returncode != 0:
        error_msg = stderr.decode(errors="replace").strip()
        logger.error(error_msg)
        raise RuntimeError(error_msg)

    logger.info(f"✅ Tayyor: {os.path.basename(output_path)}")
