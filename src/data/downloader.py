#!/usr/bin/env python3

from decouple import config
from tinydb import TinyDB


# Database
PATH = config("DATABASE_PATH")
db = TinyDB(PATH)

data = db.all()