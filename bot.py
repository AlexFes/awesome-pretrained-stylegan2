import os
import telebot
from telebot import types
import sys

sys.path.append('stylegan2')

import dnnlib
import pretrained_networks

token_list = ["1188875292:AAEsXG1kjs9kQDDeKRetB0YolucNBDrVzpg"]

for token in token_list:
    bot = telebot.TeleBot(token)

    _G, _D, Gs = pretrained_networks.load_networks('models/cat.pkl')

    def makeStartKeyboard():
        markup = types.ReplyKeyboardMarkup()
        markup.row('/Генерировать', '/Помощь')
        return markup

    @bot.message_handler(commands=['start', 'go', 'Помощь'])
    def start_handler(message):
        bot.send_message(chat_id=message.chat.id,
                         text="Stylegan2 Test",
                         reply_markup=makeStartKeyboard(),
                         parse_mode='HTML')

    @bot.message_handler(commands=['Генерировать'])
    def generate(message):
        bot.send_photo(chat_id=message.chat.id, photo=open(temp_output, "rb"))
        # send_image('cat', bot, message.chat.id)

    bot.polling()
