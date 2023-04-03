from db import session, Urls, Scraped_urls
from urllib.parse import urlparse
from pprint import pprint
from datetime import date
import urllib.request
from urllib.parse import urlparse
try:
  from bs4 import BeautifulSoup
except:
  print("You need to run `pip install beautifulsoup4`")


if (session.query(Scraped_urls).count() == 1):
  print("Good we see the scraped webpage in the database")
else:
  print("There is more than one scraped URL in the database,by the way there is a reason we don't loop through them you will learn later ")
  quit()


if (session.query(Urls).count() != 1):
  print("Seems like you already parsed all the URLs from the webpage")
  quit()

url = session.query(Urls).first()
scraped_data = session.query(Scraped_urls).where(Urls.full_url == url.full_url).first()


soup = BeautifulSoup(scraped_data.html, 'html.parser')
url_links = []
for link in soup.find_all('a'):
  FULL_URL = link.get('href')
  parsed_url = list( urlparse(link.get('href')) )
  if (parsed_url[1] == ''):
    parsed_url[1] = url.netloc
  url_links.append( [FULL_URL] + parsed_url )

url_column_dict = dict(Urls.__table__.columns)
del url_column_dict["id"]
for url in url_links:
  if len(url) == 7:
    insert_dict = {}  
    for i in range(len(list(url_column_dict))):
      print(list(url_column_dict)[i])
      insert_dict[list(url_column_dict)[i]] = url[i]
    session.add(Urls(**insert_dict))
  else:
    print(f"Error with {str(url)}")

session.commit()

print(f"URLS_T now has {session.query(Urls).count()} rows")
