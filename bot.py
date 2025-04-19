import asyncio
import os
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Update
import logging

# لاگ
logging.basicConfig(level=logging.INFO)

# دریافت توکن و آیدی گروه از متغیرهای محیطی
TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")  # مثل -1001234567890

# ایجاد scheduler
scheduler = AsyncIOScheduler()

# تابع برای ارسال پیام به گروه
async def send_message_to_group(bot: Bot):
    await bot.send_message(chat_id=GROUP_ID, text="پیام زمان‌بندی‌شده در گروه ارسال شد ✅")

# دستور استارت (تست دستی)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ربات فعال است و منتظر زمان‌بندی ✅")

# تابع اصلی
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # هندلر دستور start
    app.add_handler(CommandHandler("start", start))

    # اجرای job زمان‌بندی شده هر 10 ثانیه
    scheduler.add_job(send_message_to_group, "interval", seconds=10, args=[app.bot])
    scheduler.start()

    print("ربات در حال اجراست...")

    await app.run_polling()

# اجرای برنامه
if __name__ == "__main__":
    asyncio.run(main())
