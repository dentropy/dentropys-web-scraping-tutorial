import sqlite3
from urllib.parse import urlparse
import os
from pprint import pprint
from datetime import date
import urllib.request
from urllib.parse import urlparse
try:
  from bs4 import BeautifulSoup
except:
  print("You need to run `pip install beautifulsoup4`")

con = sqlite3.connect(f"{os.getcwd()}/scraped_data.sqlite")
cur = con.cursor()

cur.execute("SELECT COUNT(*) FROM SCRAPED_URLS_T")
if (cur.fetchone()[0] == 1):
  print("Good we see the scraped webpage in the database")
else:
  print("There is more than one scraped URL in the database,by the way there is a reason we don't loop through them you will learn later ")
  quit()


cur.execute("SELECT COUNT(*) FROM URLS_T")
if (cur.fetchone()[0] != 1):
  print("Seems like you already parsed all the URLs from teh webpage")
  quit()

cur.execute("SELECT * FROM URLS_T LIMIT 1")
keys = [description[0] for description in cur.description]
results = cur.fetchall()
pretty_results = [dict(zip(keys, row)) for row in results][0]
pprint(pretty_results)


cur.execute("SELECT HTML FROM SCRAPED_URLS_T LIMIT 1")
html_doc = cur.fetchone()[0]
soup = BeautifulSoup(html_doc, 'html.parser')
url_links = []
for link in soup.find_all('a'):
  FULL_URL = link.get('href')
  parsed_url = list( urlparse(link.get('href')) )
  if (parsed_url[1] == ''):
    parsed_url[1] = pretty_results["DOMAIN"]
  url_links.append( [FULL_URL] + parsed_url )
cur.executemany("""
  INSERT INTO URLS_T(FULL_URL, SCHEMA, DOMAIN, PATH, PARAMS, QUERY, FRAGMENT)
      VALUES (?, ?, ?, ?, ?, ?, ?)
""", url_links)
con.commit()


cur.execute("SELECT COUNT(*) FROM URLS_T")
print(f"URLS_T now has {cur.fetchone()[0]} rows")
