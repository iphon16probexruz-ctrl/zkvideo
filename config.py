import os
import shutil
import logging

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────
#  BOT TOKEN (.env dan olinadi)
# ─────────────────────────────────────────
TOKEN: str = os.getenv("BOT_TOKEN", "")

if not TOKEN:
    raise ValueError("❌ BOT_TOKEN topilmadi! .env faylga yozing.")

# ─────────────────────────────────────────
#  PATH SOZLAMALARI
# ─────────────────────────────────────────
BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR: str = os.path.join(BASE_DIR, "assets")
TEMP_DIR: str = os.path.join(BASE_DIR, "temp")

os.makedirs(TEMP_DIR, exist_ok=True)

# ─────────────────────────────────────────
#  LOGO
# ─────────────────────────────────────────
LOGO_PATH: str = os.path.join(ASSETS_DIR, "logo.png")

if not os.path.exists(LOGO_PATH):
    raise FileNotFoundError(f"❌ Logo topilmadi: {LOGO_PATH}")

# ─────────────────────────────────────────
#  FFMPEG — Windows ham Linux ham ishlaydi
# ─────────────────────────────────────────
FFMPEG_PATH: str = shutil.which("ffmpeg") or "ffmpeg"

logger.info(f"✅ FFmpeg topildi: {FFMPEG_PATH}")

# ─────────────────────────────────────────
#  VIDEO SOZLAMALARI
# ─────────────────────────────────────────
CRF: int = int(os.getenv("CRF", "22"))
PRESET: str = os.getenv("PRESET", "ultrafast")

# ─────────────────────────────────────────
#  DVD BOUNCE TEZLIGI
# ─────────────────────────────────────────
VX: int = int(os.getenv("VX", "6"))
VY: int = int(os.getenv("VY", "6"))
