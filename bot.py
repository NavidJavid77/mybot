import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging
import os

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# توکن ربات از محیط
TOKEN = os.getenv("BOT_TOKEN")

# Scheduler
scheduler = AsyncIOScheduler()

# دستور استارت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من رباتم و دارم کار می‌کنم ✅")

# یک وظیفه تست برنامه‌ریزی‌شده
def scheduled_job():
    print("🕒 اجرای زمان‌بندی‌شده")

# تابع main
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # اجرای job زمان‌بندی شده هر ۱۰ ثانیه
    scheduler.add_job(scheduled_job, "interval", seconds=10)
    scheduler.start()

    print("ربات در حال اجراست...")

    # اجرای polling
    await app.run_polling()

# اجرا
if __name__ == "__main__":
    asyncio.run(main())
