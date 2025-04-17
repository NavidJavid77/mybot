from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler

TOKEN = 'YOUR-TOKEN' 

async def start(update, context):
    await update.message.reply_text("BOT RUNNING..)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

app.run_polling()
