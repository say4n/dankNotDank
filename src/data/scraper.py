#!/usr/bin/env python3

from decouple import config
import praw
import pdb
from tinydb import TinyDB


""" Config """
# Client
CLIENT_ID = config("CLIENT_ID")
CLIENT_SECRET = config("CLIENT_SECRET")


# Developer
PASSWORD = config("PASSWORD")
USERNAME = config("USERNAME")


# Bot
USERAGENT = config("USERAGENT")
BOT_USERNAME = config("BOT_USERNAME")


# Data
PATH = config("DATABASE_PATH")
db = TinyDB(PATH)
db.purge()
cnt = len(db.all())
FILE_TYPES = [".jpg", ".jpeg", ".png"]


# PRAW
reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     password=PASSWORD,
                     user_agent=USERAGENT,
                     username=USERNAME)

subs = ["dankmemes", "memes", "funny", "dank_meme"]


def process_subreddit(sub):
    global cnt

    subreddit = reddit.subreddit(sub)

    for submission in subreddit.top(limit=None):
        # pdb.set_trace()
        try:
            data = {
                "title": submission.title,
                "thumbnail": {
                    "thumbnail": submission.thumbnail,
                    "height": submission.thumbnail_height,
                    "width": submission.thumbnail_width
                },
                "created_utc": submission.created_utc,
                "author": str(submission.author),
                "id": submission.id,
                "ups": submission.ups,
                "downs": submission.downs,
                "media": submission.url,
                "preview": submission.preview
            }

            if any(submission.url.endswith(filetype) for filetype in
                   FILE_TYPES):
                db.insert(data)
                cnt += 1

                print(f"\rProcessed {cnt} items", end='')
        except Exception as e:
            print(e)


if __name__ == "__main__":
    for sub in subs:
        process_subreddit(sub)

    print("\nDone")
