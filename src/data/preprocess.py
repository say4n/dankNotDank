#!/usr/bin/env python3

from decouple import config
import pdb
from tinydb import TinyDB

# Data
PATH = config("DATABASE_PATH")
db = TinyDB(PATH)

MEME_DB_PATH = config("MEME_LOOKUP_DB")
meme_db = TinyDB(MEME_DB_PATH)
meme_db.purge()


if __name__ == '__main__':
    max_ups = 0

    for item in db:
        max_ups = max(max_ups, item['ups'])

    for item in db:
        item['normalised_vote'] = item['ups'] / max_ups

        meme_db.insert(item)

    print("Done")
