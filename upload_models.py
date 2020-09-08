import json
import os
import sys
import shutil
import tempfile
import requests
from pathlib import Path
from config import config

def download(url, dest_path):
    """Downloads a model file and saves to dest_path.
    Can deal with normal urls and google drive and mega"""
    print(f'Downloading {dest_path} model')

    r = requests.get(url)
    downloaded_file = 'downloaded.pkl'
    with open(downloaded_file, 'wb') as f:
        f.write(r.content)

    downloaded_file = Path(downloaded_file)
    shutil.copyfile(downloaded_file, dest_path)

def main(models_dir):
    for model in config:
        model_location = Path(models_dir + "/" + model["model"] + ".pkl")
        download(model["download_url"], model_location)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        Path(sys.argv[1]).mkdir(parents=True, exist_ok=True)
        main(sys.argv[1])
    else:
        print("Expected cmd line arg: path to models directory")
