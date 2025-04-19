import requests
import jdatetime
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

# مقادیر زیر رو با مقدار واقعی جایگزین کن
BOT_TOKEN = 'BOT_TOKEN'
CHAT_ID = 'CHAT_ID'

def send_daily_message():
    # اگر امروز جمعه بود، پیام ارسال نشه
    today = jdatetime.date.today()
    if today.weekday() == 6:  # جمعه == 6
        return

    shamsi_date = today.strftime("%Y/%m/%d")
    message = f"فروش مورخ {shamsi_date}"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }

    try:
        requests.post(url, data=payload)
        print(f"پیام ارسال شد: {message}")
    except Exception as e:
        print(f"خطا در ارسال پیام: {e}")

# زمان‌بندی
scheduler = BlockingScheduler()
scheduler.add_job(send_daily_message, 'cron', hour=8, minute=30)
scheduler.start()
