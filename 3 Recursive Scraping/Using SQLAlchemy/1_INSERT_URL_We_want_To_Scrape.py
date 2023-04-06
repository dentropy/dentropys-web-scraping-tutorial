import os
from WebScrapingOrchestration import WebScrapingOrchestration
from db import Urls, Scarping_queue, Scraped_urls_logs, Url_contents
from pprint import pprint
from urllib.parse import urlparse

engine_path = "sqlite+pysqlite:///" + "/".join(os.getcwd().split("/")) + "/scraped_data.db"
wso = WebScrapingOrchestration(engine_path)

url_to_insert = "https://westworld.fandom.com/wiki/Westworld_Wiki"

if wso.session.query(Urls).where(Urls.full_url == url_to_insert).count() != 0:
  print("That URL is already in the database")
  quit()

parsed_url = urlparse(url_to_insert)
wso.session.add(Urls(
  url_to_insert,
  parsed_url.scheme,
  parsed_url.netloc,
  parsed_url.path,
  parsed_url.params,
  parsed_url.query,
  parsed_url.fragment,
))
wso.session.commit()


if wso.session.query(Urls).where(Urls.full_url == url_to_insert).count() != 0:
  print(f"Sucefully added URL={url_to_insert} to the urls table")
