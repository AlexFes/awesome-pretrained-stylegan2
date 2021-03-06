import os
import telebot
from telebot import types
import sys
from pathlib import Path
from PIL import Image
import random
import time
import config

if len(sys.argv) == 2:
    bot = telebot.TeleBot(config.token, threaded=False)
    users_data = {}

    def makeKeyboard():
        markup = types.InlineKeyboardMarkup()

        for config_item in config.config:
            markup.add(types.InlineKeyboardButton(text=config_item["model"], callback_data=config_item["model"]))

        return markup

    def makeStartKeyboard():
        markup = types.ReplyKeyboardMarkup()
        markup.row('/Генерировать', '/Помощь')
        return markup

    @bot.message_handler(commands=['start', 'go', 'Помощь'])
    def start_handler(message):
        bot.send_message(chat_id=message.chat.id,
                         text=config.start,
                         reply_markup=makeStartKeyboard(),
                         parse_mode='HTML')

    @bot.message_handler(commands=['Генерировать'])
    def generate(message):
        bot.send_message(chat_id=message.chat.id,
                         text="Генерировать:",
                         reply_markup=makeKeyboard(),
                         parse_mode='HTML')

    @bot.callback_query_handler(func=lambda call: True)
    def handle_query(call):
        dest_path = sys.argv[1] + '/{}'.format(call.data)
        images = sorted(os.listdir(dest_path))

        if not call.message.chat.id in users_data:
            users_data[call.message.chat.id] = {call.data: 0}
        elif not call.data in users_data[call.message.chat.id]:
            users_data[call.message.chat.id][call.data] = 0

        cur_img = images[users_data[call.message.chat.id][call.data]]
        users_data[call.message.chat.id][call.data] = (users_data[call.message.chat.id][call.data] + 1)%1000

        bot.send_photo(chat_id=call.message.chat.id, photo=Image.open(os.path.join(dest_path, cur_img)))

    # bot.polling(none_stop=True, interval=0, timeout=0)
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(e)
            time.sleep(15)
else:
    print("Expected cmd line arg: path to imgs directory")
