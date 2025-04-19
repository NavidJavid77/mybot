import os
import jdatetime
import pytz
import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# توکن و چت‌آی‌دی
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = -4678360479

# تابع ساختن عکس تاریخ
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

# پیام روزانه
async def send_daily_message():
    today = jdatetime.date.today().strftime("%Y/%m/%d")
    await app.bot.send_message(chat_id=CHAT_ID, text=f"فروش مورخ {today}")

    image_path = generate_date_image()
    with open(image_path, "rb") as photo:
        await app.bot.send_photo(chat_id=CHAT_ID, photo=photo)

# پیام تست برای /start
async def start(update, context):
    await update.message.reply_text("✅ ربات فعال شد!")

# زمان‌بندی فقط اگر امروز جمعه نباشه
def schedule_job():
    if jdatetime.date.today().weekday() != 6:  # 6 یعنی جمعه
        asyncio.create_task(send_daily_message())

# تنظیم زمان‌بند
scheduler = AsyncIOScheduler(timezone=pytz.timezone("Asia/Tehran"))
scheduler.add_job(schedule_job, trigger="cron", hour=8, minute=30)

# ساخت اپ و راه‌اندازی
app = ApplicationBuilder().token(TOKEN).post_init(lambda _: scheduler.start()).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
