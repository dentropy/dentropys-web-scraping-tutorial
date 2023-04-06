import os
from WebScrapingOrchestration import WebScrapingOrchestration
from db import Urls, Scarping_queue, Scraped_urls_logs, Url_contents
from pprint import pprint
import urllib.request
from datetime import datetime
import uuid
engine_path = "sqlite+pysqlite:///" + "/".join(os.getcwd().split("/")) + "/scraped_data.db"
wso = WebScrapingOrchestration(engine_path)


row_to_scrape = wso.session.query(Scarping_queue, Urls).join(Urls).order_by(Scarping_queue.priority.desc()).first()
row_to_scrape = dict(row_to_scrape[0].__dict__, **row_to_scrape[1].__dict__)


f = urllib.request.urlopen(row_to_scrape["full_url"])
contents = f.read().decode('utf-8')

content_id = str(uuid.uuid1())
wso.session.add(Url_contents(
  row_to_scrape["url_id"],
  content_id,
  contents
))
session_status = wso.session.commit()

wso.session.add(Scraped_urls_logs(
  row_to_scrape["url_id"],
  content_id,
  datetime.now(),
  "completed",
  None,
  None,
  False
))
wso.session.query(Scarping_queue).filter(Scarping_queue.id == row_to_scrape["url_id"]).delete()
wso.session.commit()

if wso.session.query(Scraped_urls_logs).count() > 0:
  tmp_url = row_to_scrape["full_url"]
  print(f"Sucefully scraped {tmp_url}")
  quit()

