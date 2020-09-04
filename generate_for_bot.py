import json
import os
import shutil
import tempfile
import requests
import subprocess
from pathlib import Path

def send_image(selected, bot, id):
    model_location = models_dir/(selected + ".pkl")
    print(model_location)
    run_network(model_location, temp_output, start_seed=0, end_seed=0)
    print(temp_output)

    # bot.send_photo(chat_id=id, photo=open(temp_output, "rb"))
    clean_up(temp_output)
