from db import Base, Urls, Scarping_queue, Scraped_urls_logs, Url_contents
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

class WebScrapingOrchestration():
  def __init__(self, engine_path):
    self.Base = Base
    self.engine = create_engine(engine_path, echo=True)
    self.Base.metadata.create_all(self.engine)
    self.session = Session(self.engine)

  def test_database_connection(self):
    query = self.session.query(Urls).limit(10)
    return query

  def insert_url(self):
    pass

  def scrape_url(self):
    pass

  def extract_urls(self):
    pass

  def insert_urls(self):
    pass

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
