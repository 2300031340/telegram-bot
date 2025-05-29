import os
from telegram.ext import Updater, MessageHandler, Filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
TRIGGER_WORD = "del"

def delete_on_trigger(update, context):
    chat_id = update.effective_chat.id
    message_text = update.message.text.lower()

    if message_text == TRIGGER_WORD:
        context.bot.send_message(chat_id, "?")
        for i in range(update.message.message_id - 1, update.message.message_id - 51, -1):
            try:
                context.bot.delete_message(chat_id=chat_id, message_id=i)
            except:
                pass

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, delete_on_trigger))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
