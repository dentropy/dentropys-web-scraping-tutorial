from db import session, Urls, Scraped_urls
from urllib.parse import urlparse

if session.query(Urls).count() != 0:
  print("There is already a URL inserted in here")
  quit()

url_to_insert = "https://westworld.fandom.com/wiki/Westworld_Wiki"
parsed_url = urlparse(url_to_insert)
session.add(Urls(
  url_to_insert,
  parsed_url.scheme,
  parsed_url.netloc,
  parsed_url.path,
  parsed_url.params,
  parsed_url.query,
  parsed_url.fragment,
))
session.commit()


if session.query(Urls).count() > 0:
  print(f"Sucefully added URL={url_to_insert} to database")
