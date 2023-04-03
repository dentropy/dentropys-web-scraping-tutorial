from db import session, Urls, Scraped_urls

query   = session.query(Urls).limit(10)
for result in query:
  pprint(result.__dict__)