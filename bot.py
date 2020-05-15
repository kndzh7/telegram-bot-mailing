# - *- coding: utf- 8 - *-
from telegram import Bot
from telegram import Update
from telegram.ext import Updater, CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.utils.request import Request

import settings


def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = "Произошла ошибка: {}".format(e)
            print(error_message)
            raise e

    return inner


@log_errors
def message(update: Update, context: CallbackContext):
    chat_id = str(update.message.chat_id)
    text = update.message.text
    if chat_id == open('admin_id.txt').read():
        text = text[9:]
        file = open('message.txt', 'w')
        file.write(text)
        file.close()
        update.message.reply_text(text="Сохранено!")


def send(update: Update, context: CallbackContext):
    chat_id = str(update.message.chat_id)
    admin_id = open('admin_id.txt').read()
    text = update.message.text
    if chat_id == admin_id:
        request = Request(connect_timeout=0.5, read_timeout=1.0)
        bot = Bot(request=request, token=settings.TOKEN)

        file = open('users.txt')
        users = file.read()
        users = users.replace(',', '')
        users = users.split()
        text = text[6:]
        for user in users:
            if user == open('admin_id.txt').read():
                pass
            else:
                bot.send_message(chat_id=user, text=text)


@log_errors
def login(update: Update, context: CallbackContext):
    chat_id = str(update.message.chat_id)
    username = update.message.from_user.username
    password = str(update.message.text[7:])
    if username == settings.LOGIN and password == settings.PASSWORD:
        update.message.reply_text(text="Добро пожаловать, господин!")
        file = open('admin_id.txt', 'w')
        file.write(chat_id)
        file.close()


@log_errors
def stats(update: Update, context: CallbackContext):
    chat_id = str(update.message.chat_id)
    if chat_id == open('admin_id.txt').read():
        file = open('users.txt')
        users = file.read()
        users = users.replace(',', '')
        users = users.split()
        text = "Количество подписчиков бота: " + str(len(users))
        update.message.reply_text(text=text)


@log_errors
def start(update: Update, context: CallbackContext):
    chat_id = str(update.message.chat_id)
    if chat_id not in open('users.txt').read():
        file = open('users.txt', 'a')
        chat_id = chat_id + ',\n'
        file.write(chat_id)
        file.close()
        update.message.reply_text(text=open('message.txt').read())


@log_errors
def help(update: Update, context: CallbackContext):
    update.message.reply_text(text=open('help.txt').read())


@log_errors
def set_help(update: Update, context: CallbackContext):
    chat_id = str(update.message.chat_id)
    text = update.message.text
    if chat_id == open('admin_id.txt').read():
        text = text[6:]
        file = open('help.txt', 'w')
        file.write(text)
        file.close()
        update.message.reply_text(text=open('help.txt').read())
        update.message.reply_text(text="Сохранено!")


@log_errors
def main():
    # 1 -- правильное подключение
    request = Request(connect_timeout=0.5, read_timeout=1.0)
    bot = Bot(request=request, token=settings.TOKEN)
    print(bot.get_me())

    # 2 -- обработчики
    updater = Updater(bot=bot, use_context=True)

    start_handler = CommandHandler('start', start)
    login_handler = CommandHandler('login', login)
    stats_handler = CommandHandler('stats', stats)
    send_handler = CommandHandler('send', send)
    start_message_handler = CommandHandler('message', message)
    help_handler = CommandHandler('help', help)
    set_help_handler = CommandHandler('set_help', set_help)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(login_handler)
    updater.dispatcher.add_handler(stats_handler)
    updater.dispatcher.add_handler(send_handler)
    updater.dispatcher.add_handler(start_message_handler)
    updater.dispatcher.add_handler(help_handler)
    updater.dispatcher.add_handler(set_help_handler)

    # 3 -- запустить бесконечную обработку входящих сообщений
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
