import os
from telegram.ext import Application

TOKEN = os.getenv("BOT_TOKEN")

application = Application.builder().token(TOKEN).build()
