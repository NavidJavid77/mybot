import os
import jdatetime
import pytz
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

TOKEN = os.getenv("BOT_TOKEN")

# گرفتن chat_id امن و مقاوم
chat_id_raw = os.getenv("GROUP_CHAT_ID")
if not chat_id_raw:
    raise Exception("❌ Environment Variable 'GROUP_CHAT_ID' is not set!")

try:
    CHAT_ID = int(chat_id_raw)
except ValueError:
    raise Exception("❌ GROUP_CHAT_ID must be a valid integer (like -1001234567890)")

# ساخت اپلیکیشن و زمان‌بندی
app = ApplicationBuilder().token(TOKEN).build()
scheduler = AsyncIOScheduler(timezone=pytz.timezone("Asia/Tehran"))

# ساخت تصویر تاریخ شمسی
def generate_date_image():
    today = jdatetime.date.today().strftime("%Y/%m/%d")
    img = Image.new("RGB", (400, 200), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # فونت ساده سیستمی (اگه فونت فارسی نداری)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font = ImageFont.truetype(font_path, 36)
    draw.text((50, 80), f"📅 {today}", font=font, fill=(0, 0, 0))

    path = "/tmp/date.jpg"
    img.save(path)
    return path

# ارسال پیام روزانه + عکس
async def send_daily_message(context: ContextTypes.DEFAULT_TYPE):
    today = jdatetime.date.today().strftime("%Y/%m/%d")
    await context.bot.send_message(chat_id=CHAT_ID, text=f"فروش مورخ {today}")

    # ارسال تصویر
    image_path = generate_date_image()
    with open(image_path, "rb") as photo:
        await context.bot.send_photo(chat_id=CHAT_ID, photo=photo)

# دستور تستی
async def start(update, context):
    await update.message.reply_text("✅ ربات فعال شد!")

async def get_chat_id(update, context):
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Chat ID: {chat_id}")

# هندلرها
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("chatid", get_chat_id))

# تنظیم زمان
scheduler.add_job(send_daily_message, trigger="cron", hour=8, minute=30)
scheduler.start()

# اجرای ربات
app.run_polling()
