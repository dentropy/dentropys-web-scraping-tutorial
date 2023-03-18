import sqlite3
from urllib.parse import urlparse
import os

con = sqlite3.connect(f"{os.getcwd()}/scraped_data.sqlite")
cur = con.cursor()

cur.execute("SELECT COUNT(*) FROM URLS_T")
if (cur.fetchone()[0] >= 1):
  print("There is already a URL inserted in here")
  quit()

url_to_insert = "https://westworld.fandom.com/wiki/Westworld_Wiki"
parsed_url = urlparse(url_to_insert)
insert_list =  [url_to_insert] + list(parsed_url)
cur.execute("""
  INSERT INTO URLS_T(FULL_URL, SCHEMA, DOMAIN, PATH, PARAMS, QUERY, FRAGMENT)
      VALUES (?, ?, ?, ?, ?, ?, ?)
""", insert_list)
con.commit()


cur.execute("SELECT COUNT(*) FROM URLS_T")
if (cur.fetchone()[0] >= 1):
  print(f"Sucefully added {url_to_insert}")
