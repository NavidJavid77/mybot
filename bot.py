import os
import jdatetime
import pytz
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

# تنظیمات ثابت
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = -4678360479

# تابع تولید عکس تاریخ
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
async def send_daily_message(context: ContextTypes.DEFAULT_TYPE):
    today = jdatetime.date.today().strftime("%Y/%m/%d")
    await context.bot.send_message(chat_id=CHAT_ID, text=f"فروش مورخ {today}")

    image_path = generate_date_image()
    with open(image_path, "rb") as photo:
        await context.bot.send_photo(chat_id=CHAT_ID, photo=photo)

# دستور استارت
async def start(update, context):
    await update.message.reply_text("✅ ربات فعاله!")

# تابع اصلی async
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    # Scheduler فقط بعد از ایجاد loop فعال
    scheduler = AsyncIOScheduler(timezone=pytz.timezone("Asia/Tehran"))
    scheduler.add_job(send_daily_message, "cron", hour=8, minute=30, args=[app])
    scheduler.start()

    print("ربات در حال اجراست...")
    await app.run_polling()

# اجرای درست با loop فعال
if __name__ == "__main__":
    asyncio.run(main())
