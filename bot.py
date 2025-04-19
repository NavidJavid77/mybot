from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Bot
from telegram.ext import Application
import asyncio

# اطلاعات ربات
TOKEN = "BOT_TOKEN"
GROUP_ID = "CHAT_ID"

async def send_message_to_group(bot: Bot):
    try:
        await bot.send_message(chat_id=GROUP_ID, text="پیام خودکار هر 10 ثانیه")
    except Exception as e:
        print(f"خطا در ارسال پیام: {e}")

async def start_bot():
    # ساخت اپلیکیشن
    app = Application.builder().token(TOKEN).build()

    # ایجاد زمان‌بندی پیام
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_message_to_group, "interval", seconds=10, args=[app.bot])
    scheduler.start()

    print("ربات در حال اجراست...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

# فقط اگر مستقیم اجرا شد (نه ایمپورت)، استارت کن
if __name__ == '__main__':
    asyncio.run(start_bot())
