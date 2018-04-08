#!/usr/bin/env python3

from decouple import config
from multiprocessing import Pool
import subprocess
from tinydb import TinyDB, Query
import wget


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
    filename = wget.download(post_url, out=output_dir)

    Post = Query()
    items = db.search(Post.id == post_id)
    item = items[0]
    item["filename"] = filename

    meme_db.insert(item)
    
    print(f"Downloaded {filename}")


if __name__ == "__main__":
    # Multiprocessing magic ✨

    with Pool(NUM_WORKERS) as p:
        p.starmap(download, meme_urls)
