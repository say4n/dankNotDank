#!/usr/bin/env python3

from decouple import config
from multiprocessing import Pool
import subprocess
from tinydb import TinyDB
import wget


# Database
PATH = config("DATABASE_PATH")
db = TinyDB(PATH)
data = db.all()

meme_urls = map(lambda submission: submission["media"], data)


# Data
OUTPUT_DIR = "memes"
subprocess.run(["mkdir", "-p", OUTPUT_DIR])


# Config
NUM_WORKERS = 8


def download(url, output_dir=OUTPUT_DIR):
    """Given an image url, save it to output_dir"""
    filename = wget.download(url, out=output_dir)
    print(f"Downloaded {filename}")

if __name__ == "__main__":
    # Multiprocessing magic ✨

    with Pool(NUM_WORKERS) as p:
        p.map(download, meme_urls)
