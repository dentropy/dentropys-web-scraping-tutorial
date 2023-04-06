from urllib.parse import urlparse
from pprint import pprint
from datetime import date
import urllib.request
from urllib.parse import urlparse
try:
  from bs4 import BeautifulSoup
except:
  print("You need to run `pip install beautifulsoup4`")

import os
from WebScrapingOrchestration import WebScrapingOrchestration
from db import Urls, Scarping_queue, Scraped_urls_logs, Url_contents
engine_path = "sqlite+pysqlite:///" + "/".join(os.getcwd().split("/")) + "/scraped_data.db"
wso = WebScrapingOrchestration(engine_path)


# Find URL that did not have the links extracted
html_contents_row = wso.session.query(Scraped_urls_logs, Urls, Url_contents)\
  .join(Urls, Scraped_urls_logs.url_id == Urls.id)\
  .join(Url_contents, Scraped_urls_logs.url_contents_id == Url_contents.content_id) \
  .filter(Scraped_urls_logs.links_extracted == False).first()
if html_contents_row == None:
  print("There are no HTML pages to scrape, or you already processed the URLs")
  quit()
html_contents_row = wso.add_dicts(html_contents_row[0].__dict__, html_contents_row[1].__dict__, html_contents_row[2].__dict__)


# Get the links
soup = BeautifulSoup(html_contents_row["html"], 'html.parser')
url_links = []
for link in soup.find_all('a'):
  # print(link)
  FULL_URL = link.get('href')
  parsed_url = list( urlparse(html_contents_row["full_url"]) )
  if (parsed_url[1] == ''):
    parsed_url[1] = url.netloc
  url_links.append( [FULL_URL] + parsed_url )

url_column_dict = dict(Urls.__table__.columns)
del url_column_dict["id"]
for url in url_links:
  if len(url) == 7:
    insert_dict = {}  
    for i in range(len(list(url_column_dict))):
      # print(list(url_column_dict)[i])
      insert_dict[list(url_column_dict)[i]] = url[i]
    wso.session.add(Urls(**insert_dict))
  else:
    print(f"Error with {str(url)}")

wso.session.commit()

log = wso.session.query(Scraped_urls_logs).filter_by(id=html_contents_row["id"]).first()
log.links_extracted = True
wso.session.commit()

print(f"URLS_T now has {wso.session.query(Urls).count()} rows")
