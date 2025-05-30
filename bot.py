import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, Filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Example: https://your-bot-service.onrender.com

app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

def delete_messages(context, chat_id, from_msg_id, count):
    for i in range(from_msg_id, from_msg_id - count, -1):
        try:
            context.bot.delete_message(chat_id=chat_id, message_id=i)
        except:
            pass

def delete_user_messages(context, chat_id, user_id):
    updates = context.bot.get_chat_history(chat_id=chat_id, limit=100)
    deleted = 0
    for msg in reversed(updates):
        if msg.from_user and msg.from_user.id == user_id:
            try:
                context.bot.delete_message(chat_id=chat_id, message_id=msg.message_id)
                deleted += 1
                if deleted >= 50:
                    break
            except:
                pass

def handle_commands(update, context):
    chat_id = update.effective_chat.id
    message_id = update.message.message_id
    message_text = update.message.text.strip().lower()

    # Command: del
    if message_text == "del":
        delete_messages(context, chat_id, message_id, 50)

    # Command: d n
    elif message_text.startswith("d "):
        try:
            n = int(message_text.split()[1])
            delete_messages(context, chat_id, message_id, n)
        except:
            pass

    # Command: dp
    elif message_text == "dp" and update.message.reply_to_message:
        try:
            # Delete the replied message
            context.bot.delete_message(chat_id=chat_id, message_id=update.message.reply_to_message.message_id)
            # Delete the command message itself
            context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        except:
            pass

    # Command: dpp
    elif message_text == "dpp" and update.message.reply_to_message:
        target_user_id = update.message.reply_to_message.from_user.id
        try:
            messages = context.bot.get_chat_history(chat_id=chat_id, limit=200)
            deleted = 0
            for msg in reversed(messages):
                if msg.from_user and msg.from_user.id == target_user_id:
                    try:
                        context.bot.delete_message(chat_id=chat_id, message_id=msg.message_id)
                        deleted += 1
                        if deleted >= 50:
                            break
                    except:
                        continue
            # Delete the "dpp" command message itself
            context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        except:
            pass

dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_commands))

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
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
