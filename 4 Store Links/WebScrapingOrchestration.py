from db import Base, Urls, Scarping_queue, Scraped_urls_logs, Url_contents, Url_links
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
from pprint import pprint

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
    """
    Check if URL in urls_t, all urls are added there after a site is scraped
    Check if URL in scraping_queue_t
    """
    join_results = self.session.query(Urls).where(Urls.full_url == url_to_join).all()
    result = self.session.query(Scarping_queue).\
      where(Scarping_queue.full_url == join_results[0].full_url).all()
    if len(result) == 0:
      self.session.add(Scarping_queue(
        join_results[0].full_url,
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
    # TODO why does this not work recursively anymore?
    row_to_scrape = self.session.query(Scarping_queue, Urls).join(Urls).order_by(Scarping_queue.priority.desc()).first()
    if row_to_scrape == None:
      return False
    row_to_scrape = dict(row_to_scrape[0].__dict__, **row_to_scrape[1].__dict__)
    content_id = ""
    try:
      f = urllib.request.urlopen(row_to_scrape["full_url"])
    except Exception as e:
      self.session.add(Scraped_urls_logs(
        row_to_scrape["full_url"],
        content_id,
        datetime.now(),
        "completed",
        0,
        str(e),
        False
      ))
      self.session.query(Scarping_queue).filter(Scarping_queue.full_url == row_to_scrape["full_url"]).delete()
      self.session.commit()
      return False
    if (f.getcode() != 200):
      self.session.add(Scraped_urls_logs(
        row_to_scrape["full_url"],
        content_id,
        datetime.now(),
        "completed",
        f.getcode(),
        None,
        False
      ))
      self.session.query(Scarping_queue).filter(Scarping_queue.full_url == row_to_scrape["full_url"]).delete()
      self.session.commit()
      return False
    contents = f.read().decode('utf-8')
    content_id = str(uuid.uuid1())
    self.session.add(Url_contents(
      row_to_scrape["full_url"],
      content_id,
      contents
    ))
    session_status = self.session.commit()

    self.session.add(Scraped_urls_logs(
      row_to_scrape["full_url"],
      content_id,
      datetime.now(),
      "completed",
      200,
      None,
      False
    ))
    self.session.query(Scarping_queue).filter(Scarping_queue.full_url == row_to_scrape["full_url"]).delete()
    self.session.commit()
    return True

  def extract_urls(self):
    # Find URL that did not have the links extracted
    html_contents_row = self.session.query(Scraped_urls_logs, Urls, Url_contents)\
      .join(Urls, Scraped_urls_logs.full_url == Urls.full_url)\
      .join(Url_contents, Scraped_urls_logs.url_contents_id == Url_contents.content_id) \
      .filter(Scraped_urls_logs.links_extracted == False).first()
    if html_contents_row == None:
      print("There are no HTML pages to scrape, or you already processed the URLs")
      quit()
    html_contents_row_dict = self.add_dicts(html_contents_row[0].__dict__, html_contents_row[1].__dict__, html_contents_row[2].__dict__)


    # Get the links
    soup = BeautifulSoup(html_contents_row_dict["html"], 'html.parser')
    url_links = []
    for link in soup.find_all('a'):
      # print(link)
      FULL_URL = link.get('href')
      if FULL_URL == None or FULL_URL == '#' or FULL_URL == '':
        continue
      parsed_url = list( urlparse(FULL_URL) )
      if (parsed_url[1] == ''):
        parsed_url[1] = urlparse(html_contents_row_dict["full_url"]).netloc
      # print("FULL_URL")
      # print(FULL_URL)
      if FULL_URL[0] == "/":
        FULL_URL = urlparse(html_contents_row_dict["full_url"]).scheme + "://" + urlparse(html_contents_row_dict["full_url"]).netloc + FULL_URL
      url_links.append( [FULL_URL] + parsed_url )

    # Format the links and save them to session

    url_column_dict = dict(Urls.__table__.columns)
    # current_url_row = session.query(Urls).filter(Urls.full_url == ).first()
    for url in url_links:
      pprint(url)
      if len(url) == 7:
        if self.session.query(Urls).filter(Urls.full_url == url[0]).count() == 0:
          insert_dict = {}  
          for i in range(len(list(url_column_dict))):
            # print(list(url_column_dict)[i])
            insert_dict[list(url_column_dict)[i]] = url[i]
          # Store the links
          url_to_add = Urls(**insert_dict)
          Url_links(html_contents_row[1], url_to_add)
          self.session.add(url_to_add)
        else:
          print(f"Error in extract_urls with {str(url)}, already in urls_t")
      else:
        print(f"Error in extract_urls processing {str(url)}")
    self.session.commit()

    log = self.session.query(Scraped_urls_logs).\
      filter(Scraped_urls_logs.full_url == html_contents_row_dict["full_url"]).first()
    log.links_extracted = True
    self.session.commit()

    print(f"URLS_T now has {self.session.query(Urls).count()} rows")
    return html_contents_row_dict["full_url"]

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


  def queue_up_urls(self, full_url, tld):
    # Find all links from full_url
    links_to_add = self.session.query(Url_links, Urls)\
      .join(Url_links, Url_links.from_url_id == Urls.full_url)\
      .filter(
        Url_links.from_url_id == full_url,
        Urls.netloc           == tld
      ).all()
    if len(links_to_add) == 0:
      return True
    # Check if links are in Scraped_urls_logs or Scarping_queue
    for tmp_url in links_to_add:
      if tld not in str(tmp_url[0].to_url_id):
        continue
      Scraped_url_count = self.session.query(Scraped_urls_logs).\
        filter(Scraped_urls_logs.full_url == tmp_url[0].to_url_id).count()
      Scraped_logs_count = self.session.query(Scarping_queue).\
        filter(Scarping_queue.full_url == tmp_url[0].to_url_id).count()
      pprint(f"Scraped_url_count = {Scraped_url_count}")
      pprint(f"Scraped_logs_count = {Scraped_logs_count}")
      if Scraped_url_count == 0 and Scraped_logs_count == 0:
        self.add_url_to_scraping_queue(tmp_url[0].to_url_id)
    # Add Urls to scraping queue


  def recursive_scraping(self, url_to_scrape, recursive_limit):
    tld = urlparse(url_to_scrape).netloc
    self.insert_url(url_to_scrape)
    self.add_url_to_scraping_queue(url_to_scrape)
    scraping_status = True
    while scraping_status != "":
      scraped_count = self.session.query(Scraped_urls_logs).count()
      pprint(f"scraped_count = {scraped_count}")
      if scraped_count > recursive_limit:
        print(f"Logs indicate scraped over {recursive_limit} pages, which is the limit you set")
        quit() 
      scraping_status = self.scrape_url()
      if scraping_status == False:
        continue
      pprint(f"scraping_status = {scraping_status}")
      full_url = self.extract_urls()
      pprint(f"my_full_url = {full_url}")  
      self.queue_up_urls(str(full_url), tld)
    print("Done Scraping")