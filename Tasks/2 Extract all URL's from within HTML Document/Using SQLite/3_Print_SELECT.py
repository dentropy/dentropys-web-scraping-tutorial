import sqlite3
import os
from urllib.parse import urlparse
from pprint import pprint

con = sqlite3.connect(f"{os.getcwd()}/scraped_data.sqlite")
cur = con.cursor()
cur.execute("SELECT * FROM URLS_T LIMIT 1")
keys = [description[0] for description in cur.description]
results = cur.fetchall()
pretty_results = [dict(zip(keys, row)) for row in results]
pprint(pretty_results[0])
