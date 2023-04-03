import sqlite3
from urllib.parse import urlparse
import os
from pprint import pprint
from datetime import date
import urllib.request
con = sqlite3.connect(f"{os.getcwd()}/scraped_data.sqlite")
cur = con.cursor()

cur.execute("SELECT COUNT(*) FROM SCRAPED_URLS_T")
if (cur.fetchone()[0] >= 1):
  print("You already scraped a URL")
  quit()

cur.execute("SELECT COUNT(*) FROM URLS_T")
if (cur.fetchone()[0] != 1):
  print("There is more than one URL to scrape, by the way there is a reason we don't loop through them you will learn later")
  quit()

cur.execute("SELECT * FROM URLS_T")
keys = [description[0] for description in cur.description]
results = cur.fetchall()
pretty_results = [dict(zip(keys, row)) for row in results][0]
pprint(pretty_results)

f = urllib.request.urlopen(pretty_results["FULL_URL"])
contents = f.read().decode('utf-8')

insert_list =  [ pretty_results["URL_ID"], date.today(), contents]
cur.execute(f"""
  INSERT INTO SCRAPED_URLS_T(URL_ID, DATE_SCRAPED, HTML)
      VALUES (?, ?, ?)
""", insert_list)
con.commit()


cur.execute("SELECT COUNT(*) FROM SCRAPED_URLS_T")
if (cur.fetchone()[0] >= 1):
  tmp = pretty_results["FULL_URL"]
  print(f"Sucefully scraped {tmp}")
