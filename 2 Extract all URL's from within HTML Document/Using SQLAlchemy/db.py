import os
from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship, Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine_path = "sqlite+pysqlite:///" + "/".join(os.getcwd().split("/")) + "/scraped_data.db"
engine = create_engine(engine_path, echo=True)

Base = declarative_base()

class Urls(Base):
   __tablename__ = 'urls_t'
   id = Column(Integer, primary_key=True)

   full_url          = Column(String)
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


class Scraped_urls(Base):
   __tablename__ = 'scraped_urls_t'
   id = Column(Integer, primary_key=True)

   url_id          = Column(Integer, ForeignKey('urls_t.id'))
   date_scraped    = Column(Date())
   html             = Column(Text())

   def __init__(self, url_id, date_scraped, html):
      self.url_id        = url_id
      self.date_scraped  = date_scraped
      self.html          = html

Base.metadata.create_all(engine)
session = Session(engine)
