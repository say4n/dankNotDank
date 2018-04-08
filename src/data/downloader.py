#!/usr/bin/env python3

from decouple import config
from multiprocessing import Pool
import subprocess
from tinydb import TinyDB, Query
import wget


# Database
PATH = config("DATABASE_PATH")
db = TinyDB(PATH)
data = db.all()

meme_urls = map(lambda submission: (submission["id"], submission["media"]),
                data)


# Data
OUTPUT_DIR = "memes"
subprocess.run(["mkdir", "-p", OUTPUT_DIR])


# Config
NUM_WORKERS = 8


def download(post_id, post_url, output_dir=OUTPUT_DIR):
    """Given an image url, save it to output_dir"""
    filename = wget.download(post_url, out=output_dir)

    Post = Query()
    db.update({"filename": filename}, Post.id == post_id)
    
    print(f"Downloaded {filename}")


if __name__ == "__main__":
    # Multiprocessing magic ✨

    with Pool(NUM_WORKERS) as p:
        p.map(download, meme_urls)
