import os
import telebot
from telebot import types
import sys
from pathlib import Path
import random
import config
import threading

sys.path.append('stylegan2')

import dnnlib
import dnnlib.tflib as tflib
import numpy as np

def generate_images(model_path, dest_path, seed_range):
    threading.Timer(60.0 * 60.0, generate_images).start()

    sc = dnnlib.SubmitConfig()
    sc.num_gpus = 1
    sc.submit_target = dnnlib.SubmitTarget.LOCAL
    sc.local.do_not_copy_source_files = True
    sc.run_dir_root = './stylegan2/results'
    sc.run_desc = 'generate_images'

    dnnlib.submit_run(sc, 'run_generator.generate_images', network_pkl=model_path, seeds=range(seed_range), truncation_psi=1.0, dest=dest_path)

if (len(sys.argv) == 3)
    for config_item in config.config:
        model_path = sys.argv[1] + '/{}.pkl'.format(config_item["model"])
        dest_path = sys.argv[2] + '/{}'.format(config_item["model"])
        seed_range = 1000
        Path(dest_path).mkdir(parents=True, exist_ok=True)
        generate_images(model_path, dest_path, seed_range)

    bot = telebot.TeleBot(config.token)

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
        dest_path = sys.argv[2] + '/{}'.format(call.data)
        images = os.listdir(dest_path)
        cur_img = random.choice(images)
        bot.send_photo(chat_id=call.message.chat.id, photo=open(os.path.join(dest_path, cur_img), "rb"))

    bot.polling(none_stop=True, interval=0, timeout=0)

else:
    print("Expected cmd line args: path to models directory; path to imgs directory")
