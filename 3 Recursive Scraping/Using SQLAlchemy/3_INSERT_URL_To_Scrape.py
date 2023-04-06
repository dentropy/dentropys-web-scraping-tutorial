import os
from WebScrapingOrchestration import WebScrapingOrchestration
from db import Urls, Scarping_queue, Scraped_urls_logs, Url_contents
from pprint import pprint
from urllib.parse import urlparse
from datetime import datetime
engine_path = "sqlite+pysqlite:///" + "/".join(os.getcwd().split("/")) + "/scraped_data.db"
wso = WebScrapingOrchestration(engine_path)

url_to_join = "https://westworld.fandom.com/wiki/Westworld_Wiki"

join_results = wso.session.query(Urls).where(Urls.full_url == url_to_join).all()
if len(join_results) == 0:
  print("Can't find the URL you requested in the database, please run previous commands")
  quit()

result = wso.session.query(Scarping_queue).where(Scarping_queue.url_id == join_results[0].id).all()
if len(result) == 0:
  wso.session.add(Scarping_queue(
    join_results[0].id,
    255,             # priority
    datetime.now(),  # datetime_to_scrape
    "requests",      # scape_mode
    "TODO"           # status     
  ))
  wso.session.commit()
else:
  print("You already have that URL queued up")
  quit()

if wso.session.query(Scarping_queue).where(Scarping_queue.url_id == join_results[0].id).count() != 0:
  print(f"Sucefully added URL={url_to_join} to scraping_queue table")
