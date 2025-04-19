import os
import jdatetime
import pytz
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

# گرفتن توکن و چت آیدی از متغیر محیطی
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("GROUP_CHAT_ID"))  # عددی که از گروه گرفتی

# ساخت اپلیکیشن تلگرام
app = ApplicationBuilder().token(TOKEN).build()

# زمان‌بندی
scheduler = AsyncIOScheduler(timezone=pytz.timezone("Asia/Tehran"))

# تابع برای فرستادن پیام روزانه
async def send_daily_message(context: ContextTypes.DEFAULT_TYPE):
    today = jdatetime.date.today().strftime("%Y/%m/%d")
    text = f"فروش مورخ {today}"
    
    # ارسال پیام به گروه
    await context.bot.send_message(chat_id=CHAT_ID, text=text)
    
    # می‌تونی اینجا استیکر هم اضافه کنی:
    # await context.bot.send_sticker(chat_id=CHAT_ID, sticker='STICKER_FILE_ID')

# فرمان /start فقط برای تست
async def start(update, context):
    await update.message.reply_text("ربات فعاله ✅")

# ثبت هندلر
app.add_handler(CommandHandler("start", start))

# زمان‌بندی هر روز ساعت ۸:۳۰ صبح
scheduler.add_job(send_daily_message, trigger="cron", hour=8, minute=30)
scheduler.start()

# اجرای ربات
app.run_polling()
