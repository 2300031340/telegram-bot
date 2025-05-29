import os
from telegram.ext import Updater, MessageHandler, Filters
from flask import Flask, request

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # e.g., https://your-bot-service.onrender.com
TRIGGER_WORD = "del"

from telegram import Bot, Update
from telegram.ext import Dispatcher

app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

def delete_on_trigger(update, context):
    chat_id = update.effective_chat.id
    message_id = update.message.message_id
    message_text = update.message.text.lower()

    if message_text == TRIGGER_WORD:
        try:
            context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        except:
            pass
        for i in range(message_id - 1, message_id - 51, -1):
            try:
                context.bot.delete_message(chat_id=chat_id, message_id=i)
            except:
                pass

dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, delete_on_trigger))

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

@app.route('/')
def index():
    return "Bot is running"

if __name__ == "__main__":
    bot.delete_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{BOT_TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
