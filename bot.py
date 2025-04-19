import os
import jdatetime
import pytz
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

TOKEN = os.getenv("BOT_TOKEN")

# chat_id به صورت مستقیم (ثابت گذاشتیم چون الان می‌دونیم چنده)
CHAT_ID = -4678360479

# ساخت اپلیکیشن و زمان‌بندی
app = ApplicationBuilder().token(TOKEN).build()
scheduler = AsyncIOScheduler(timezone=pytz.timezone("Asia/Tehran"))

# ساخت تصویر تاریخ شمسی
def generate_date_image():
    today = jdatetime.date.today().strftime("%Y/%m/%d")
    img = Image.new("RGB", (400, 200), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

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

# هندلرها
app.add_handler(CommandHandler("start", start))

# تنظیم زمان روزانه به جز جمعه
def is_not_friday():
    return jdatetime.date.today().weekday() != 6  # جمعه = 6 در تقویم جلالی

def scheduled_job():
    if is_not_friday():
        return send_daily_message

scheduler.add_job(send_daily_message, trigger="cron", hour=8, minute=30)
scheduler.start()

# اجرای ربات
app.run_polling()
