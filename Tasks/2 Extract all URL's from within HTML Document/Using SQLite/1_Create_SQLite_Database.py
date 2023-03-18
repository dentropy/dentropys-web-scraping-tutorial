import os
import sqlite3

con = sqlite3.connect(f"{os.getcwd()}/scraped_data.sqlite")
cur = con.cursor()
cur.execute("""
  CREATE TABLE IF NOT EXISTS SCRAPED_URLS_T(
    SCRAPED_URL_ID   INTEGER PRIMARY KEY,
    URL_ID           INTEGER,
    DATE_SCRAPED     DATE,
    HTML             TEXT
  )
""")
con.commit()
cur.execute("""
  CREATE TABLE IF NOT EXISTS URLS_T(
    URL_ID           INTEGER PRIMARY KEY,
    FULL_URL         TEXT,
    SCHEMA           TEXT,
    DOMAIN           TEXT,
    PATH             TEXT,
    PARAMS           TEXT,
    QUERY            TEXT,
    FRAGMENT         TEXT
  )
""")
con.commit()
