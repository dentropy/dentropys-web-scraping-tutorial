from db import Base, Urls, Scarping_queue, Scraped_urls_logs, Url_contents
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from urllib.parse import urlparse
import uuid
from datetime import datetime
import urllib.request
from urllib.parse import urlparse
try:
  from bs4 import BeautifulSoup
except:
  print("You need to run `pip install beautifulsoup4`")

class WebScrapingOrchestration():
  def __init__(self, engine_path):
    self.Base = Base
    self.engine = create_engine(engine_path, echo=True)
    self.Base.metadata.create_all(self.engine)
    self.session = Session(self.engine)

  def test_database_connection(self):
    query = self.session.query(Urls).limit(10)
    return query

  def insert_url(self, url_to_insert):
    if self.session.query(Urls).where(Urls.full_url == url_to_insert).count() != 0:
      return False
    parsed_url = urlparse(url_to_insert)
    self.session.add(Urls(
      url_to_insert,
      parsed_url.scheme,
      parsed_url.netloc,
      parsed_url.path,
      parsed_url.params,
      parsed_url.query,
      parsed_url.fragment,
    ))
    self.session.commit()
    return True

  def add_url_to_scraping_queue(self, url_to_join):
    join_results = self.session.query(Urls).where(Urls.full_url == url_to_join).all()
    result = self.session.query(Scarping_queue).where(Scarping_queue.url_id == join_results[0].id).all()
    if len(result) == 0:
      self.session.add(Scarping_queue(
        join_results[0].id,
        255,             # priority
        datetime.now(),  # datetime_to_scrape
        "requests",      # scape_mode
        "TODO"           # status     
      ))
      self.session.commit()
      return(True)
    else:
      return("You already have that URL queued up")

  def scrape_url(self):
    row_to_scrape = self.session.query(Scarping_queue, Urls).join(Urls).order_by(Scarping_queue.priority.desc()).first()
    row_to_scrape = dict(row_to_scrape[0].__dict__, **row_to_scrape[1].__dict__)
    f = urllib.request.urlopen(row_to_scrape["full_url"])
    if (f.getcode() != 200):
      self.session.add(Scraped_urls_logs(
        row_to_scrape["url_id"],
        content_id,
        datetime.now(),
        "completed",
        f.getcode(),
        None,
        False
      ))
      self.session.query(Scarping_queue).filter(Scarping_queue.id == row_to_scrape["url_id"]).delete()
      self.session.commit()
      return False
    contents = f.read().decode('utf-8')
    content_id = str(uuid.uuid1())
    self.session.add(Url_contents(
      row_to_scrape["url_id"],
      content_id,
      contents
    ))
    session_status = self.session.commit()

    self.session.add(Scraped_urls_logs(
      row_to_scrape["url_id"],
      content_id,
      datetime.now(),
      "completed",
      200,
      None,
      False
    ))
    self.session.query(Scarping_queue).filter(Scarping_queue.id == row_to_scrape["url_id"]).delete()
    self.session.commit()

    if self.session.query(Scraped_urls_logs).count() > 0:
      return False
    return True

  def extract_urls(self):
    # Find URL that did not have the links extracted
    html_contents_row = self.session.query(Scraped_urls_logs, Urls, Url_contents)\
      .join(Urls, Scraped_urls_logs.url_id == Urls.id)\
      .join(Url_contents, Scraped_urls_logs.url_contents_id == Url_contents.content_id) \
      .filter(Scraped_urls_logs.links_extracted == False).first()
    if html_contents_row == None:
      print("There are no HTML pages to scrape, or you already processed the URLs")
      quit()
    html_contents_row = self.add_dicts(html_contents_row[0].__dict__, html_contents_row[1].__dict__, html_contents_row[2].__dict__)


    # Get the links
    soup = BeautifulSoup(html_contents_row["html"], 'html.parser')
    url_links = []
    for link in soup.find_all('a'):
      # print(link)
      FULL_URL = link.get('href')
      if FULL_URL == None or FULL_URL == '#':
        continue
      parsed_url = list( urlparse(FULL_URL) )
      if (parsed_url[1] == ''):
        parsed_url[1] = urlparse(html_contents_row["full_url"]).netloc
      print("FULL_URL")
      print(FULL_URL)
      if FULL_URL[0] == "/":
        FULL_URL = urlparse(html_contents_row["full_url"]).scheme + "://" + urlparse(html_contents_row["full_url"]).netloc + FULL_URL
      url_links.append( [FULL_URL] + parsed_url )
    url_column_dict = dict(Urls.__table__.columns)
    del url_column_dict["id"]
    for url in url_links:
      if len(url) == 7:
        insert_dict = {}  
        for i in range(len(list(url_column_dict))):
          # print(list(url_column_dict)[i])
          insert_dict[list(url_column_dict)[i]] = url[i]
        self.session.add(Urls(**insert_dict))
      else:
        print(f"Error with {str(url)}")

    self.session.commit()

    log = self.session.query(Scraped_urls_logs).filter_by(id=html_contents_row["id"]).first()
    log.links_extracted = True
    self.session.commit()

    print(f"URLS_T now has {self.session.query(Urls).count()} rows")
    return True

  def add_dicts(self, *dicts): # Thanks ChatGPT
      """
      Add multiple dictionaries together and remove duplicate values.
      """
      result = {}
      for d in dicts:
          for k, v in d.items():
              if k in result and result[k] == v:
                  continue
              else:
                  result[k] = v
      return result

  def recursive_scraping(self, tld, recursive_limit):
    # self.session.query(Scraped_urls_logs).count() < recursive_limit:
    # Get all URL's that have tld in URL's table and add to queue
    urls_to_add = self.session.query(Urls).filter(Urls.netloc == tld)
    for url in urls_to_add:
      print(url.full_url)
      # self.add_url_to_scraping_queue(url.full_url)
    # churn through queue until 0
