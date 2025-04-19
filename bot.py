import asyncio
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from telegram import Bot
from telegram.ext import Application

# تابع برای ارسال پیام به گروه
async def send_message_to_group(bot: Bot):
    chat_id = 'CHAT_ID'  # شناسه گروه خود را وارد کنید
    message = "این پیام هر 10 ثانیه یکبار ارسال می‌شود."
    await bot.send_message(chat_id=chat_id, text=message)

# تابع اصلی که در آن برنامه‌ریزی می‌کنیم
async def main():
    # ایجاد شیء Application
    app = Application.builder().token('BOT_TOKEN').build()

    # راه‌اندازی برنامه‌ریز
    scheduler = AsyncIOScheduler(timezone=pytz.UTC)  # استفاده از pytz.UTC به عنوان تایم‌زون معتبر
    scheduler.add_job(send_message_to_group, IntervalTrigger(seconds=10), args=[app.bot])

    # شروع برنامه‌ریز
    scheduler.start()

    # اجرای polling برای ربات
    await app.run_polling()

# اجرای برنامه اصلی
if __name__ == "__main__":
    asyncio.run(main())
