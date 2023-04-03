from db import session, Urls, Scraped_urls
from urllib.parse import urlparse
import urllib.request
from pprint import pprint
from datetime import datetime

if session.query(Scraped_urls).count() != 0:
  print("You already scraped a URL")
  quit()

if session.query(Urls).count() != 1:
  print("There is more than one URL to scrape, by the way there is a reason we don't loop through them you will learn later")
  quit()

url = session.query(Urls).first()
pprint(url.__dict__)

f = urllib.request.urlopen(url.full_url)
contents = f.read().decode('utf-8')


session.add(Scraped_urls(
  url.id,
  datetime.now(),
  contents
))
session.commit()


if session.query(Urls).count() > 0:
  print(f"Sucefully scraped {url.full_url}")
  quit()
