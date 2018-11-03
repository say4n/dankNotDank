from decouple import config
import matplotlib.pyplot as plt
import numpy as np
from tinydb import TinyDB, Query


# Database
PATH = config("DATABASE_PATH")
db = TinyDB(PATH)

data = db.all()

upvotes = [record['ups'] for record in data]


hist, bins, _ = plt.hist(upvotes)
plt.clf()
logbins = np.logspace(np.log10(bins[0]), np.log10(bins[-1]), len(bins))
plt.hist(upvotes, bins=logbins)

plt.ylabel("# of Posts")
plt.xlabel("# of Upvotes")
plt.title("Distribution of Upvotes")

plt.show()
