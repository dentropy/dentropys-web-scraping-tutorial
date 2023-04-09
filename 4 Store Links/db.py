import os
from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Urls(Base):
   __tablename__ = 'urls_t'
   full_url          = Column(String, primary_key=True)
   scheme            = Column(String)
   netloc            = Column(String)
   path              = Column(String)
   params            = Column(String)
   query             = Column(String)
   fragment          = Column(String)

   def __init__(self, full_url, scheme, netloc, path, params, query, fragment):
        self.full_url = full_url
        self.scheme   = scheme
        self.netloc   = netloc
        self.path     = path
        self.params   = params
        self.query    = query
        self.fragment = fragment

   def higher_neighbors(self):
      return [x.from_url_node for x in self.from_url_edge]

   def lower_neighbors(self):
      return [x.to_url_node for x in self.to_url_edge]

# [examples.graphs.directed\_graph — SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/_modules/examples/graphs/directed_graph.html)
class Url_links(Base):
    __tablename__ = "url_links_t"
    from_url_id = Column(Integer, ForeignKey("urls_t.full_url"), primary_key=True)
    to_url_id   = Column(Integer, ForeignKey("urls_t.full_url"), primary_key=True)
    from_url_node = relationship(
        Urls,  primaryjoin=from_url_id == Urls.full_url, backref="from_url_edge"
    )
    to_url_node = relationship(
        Urls,  primaryjoin=to_url_id == Urls.full_url, backref="to_url_edge"
    )
    def __init__(self, from_url, to_url):
        self.from_url_node = from_url
        self.to_url_node   = to_url

class Scarping_queue(Base):
   __tablename__ = 'scraping_queue_t'
   id = Column(Integer, primary_key=True)

   full_url           = Column(String, ForeignKey('urls_t.full_url'))
   priority           = Column(Integer)
   datetime_to_scrape = Column(Date)
   scrape_mode        = Column(String)
   status             = Column(String)

   def __init__(self, full_url, priority, datetime_to_scrape, scrape_mode, status):
      self.full_url            = full_url
      self.priority            = priority
      self.datetime_to_scrape  = datetime_to_scrape
      self.scrape_mode         = scrape_mode
      self.status              = status

class Scraped_urls_logs(Base):
   __tablename__ = 'scraped_urls_logs_t'
   id = Column(Integer, primary_key=True)

   full_url             = Column(String, ForeignKey('urls_t.full_url'))
   url_contents_id      = Column(Integer, ForeignKey('url_contents_t.content_id'))
   datetime_scraped     = Column(Date)
   status               = Column(String)
   response_code        = Column(Integer)
   error_description    = Column(String)
   links_extracted      = Column(Boolean)

   def __init__(self, full_url, url_contents_id, datetime_scraped, status, response_code, error_description, links_extracted):
      self.full_url             = full_url
      self.url_contents_id      = url_contents_id
      self.datetime_scraped     = datetime_scraped
      self.status               = status
      self.response_code        = response_code
      self.error_description    = error_description
      self.links_extracted      = links_extracted

class Url_contents(Base):
   __tablename__ = 'url_contents_t'
   id = Column(Integer, primary_key=True)

   full_url    = Column(String, ForeignKey('urls_t.full_url'))
   content_id  = Column(String)
   html        = Column(Text)

   def __init__(self, full_url, content_id, html):
      self.full_url      = full_url
      self.content_id    = content_id
      self.html          = html


# To use db.py separately you need the following lines in your code

# engine_path = "sqlite+pysqlite:///" + "/".join(os.getcwd().split("/")) + "/scraped_data.db"
# engine = create_engine(engine_path, echo=True)
# Base.metadata.create_all(engine)
# session = Session(engine)
