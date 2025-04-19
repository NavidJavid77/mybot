import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Bot
from telegram.ext import Application

# توکن ربات تلگرام و آیدی گروه
TOKEN = "BOT_TOKEN"
GROUP_ID = "CHAT_ID"

async def send_message_to_group(bot: Bot):
    try:
        await bot.send_message(GROUP_ID, "پیام خودکار هر 10 ثانیه")
    except Exception as e:
        print(f"خطا در ارسال پیام: {e}")

async def main():
    # ایجاد اپلیکیشن و ربات تلگرام
    app = Application.builder().token(TOKEN).build()

    # ایجاد یک شیء از AsyncIOScheduler
    scheduler = AsyncIOScheduler()

    # تنظیم زمان‌بندی ارسال پیام هر 10 ثانیه
    scheduler.add_job(send_message_to_group, "interval", seconds=10, args=[app.bot])
    scheduler.start()

    # شروع به کار کردن اپلیکیشن
    await app.run_polling()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
