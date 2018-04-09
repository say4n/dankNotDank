#!/usr/bin/env python3

from decouple import config
from multiprocessing import Pool
import os
import shutil
import subprocess
from tinydb import TinyDB, Query
from urllib.request import urlopen
from urllib.parse import urlparse


# Data
OUTPUT_DIR = "memes"
subprocess.run(["mkdir", "-p", OUTPUT_DIR])


# Database
PATH = config("DATABASE_PATH")
db = TinyDB(PATH)
data = db.all()

MEME_LOOKUP_DB = config("MEME_LOOKUP_DB")
meme_db = TinyDB(MEME_LOOKUP_DB)

meme_urls = map(lambda submission: (submission["id"], submission["media"]),
                data)


# Config
NUM_WORKERS = 8


def download(post_id, post_url, output_dir=OUTPUT_DIR):
    """Given an image url, save it to output_dir"""
    *_, extension = os.path.basename(urlparse(post_url).path).split('.')
    output_filename = os.path.join(output_dir, f"{post_id}.{extension}")
    
    # Download the file from `url` and save it locally under `output_filename`:    
    with urlopen(post_url) as response, open(output_filename, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    
    print(f"Downloaded {output_filename}")


if __name__ == "__main__":
    # Multiprocessing magic ✨
    with Pool(NUM_WORKERS) as p:
        p.starmap(download, meme_urls)
