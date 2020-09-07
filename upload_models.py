import json
import os
import shutil
import tempfile
import requests
from pathlib import Path
from config import config

models_dir = Path('models')

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

def main():
    for model in config:
        model_location = models_dir/(model["model"] + ".pkl")
        download(model["download_url"], model_location)

if __name__ == "__main__":
    models_dir.mkdir(parents=True, exist_ok=True)
    main()
