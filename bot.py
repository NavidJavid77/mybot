import os
import jdatetime
import pytz
import asyncio
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# اطلاعات ثابت
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = -4678360479  # چت آیدی گروهت

# ساخت تصویر تاریخ
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

# ارسال پیام روزانه
async def send_daily_message(app):
    today = jdatetime.date.today().strftime("%Y/%m/%d")
    await app.bot.send_message(chat_id=CHAT_ID, text=f"فروش مورخ {today}")

    image_path = generate_date_image()
    with open(image_path, "rb") as photo:
        await app.bot.send_photo(chat_id=CHAT_ID, photo=photo)

# استارت هندلر
async def start(update, context):
    await update.message.reply_text("✅ ربات فعال است!")

# تابع اصلی
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    # زمان‌بندی پیام روزانه فقط اگر جمعه نیست
    scheduler = AsyncIOScheduler(timezone=pytz.timezone("Asia/Tehran"))
    scheduler.add_job(lambda: asyncio.create_task(send_daily_message(app)), trigger="cron", hour=8, minute=30)
    scheduler.start()

    print("ربات در حال اجراست...")
    await app.run_polling()

# اجرای برنامه
if __name__ == "__main__":
    asyncio.run(main())
