from sqlalchemy import create_engine, MetaData
import os

# set up the connection to the database
engine_path = "sqlite+pysqlite:///" + "/".join(os.getcwd().split("/")) + "/scraped_data.db"
engine = create_engine(engine_path)
conn = engine.connect()

# get all table names
meta = MetaData()
meta.reflect(bind=engine)
table_names = meta.tables.keys()

# loop through and drop each table
for table_name in table_names:
    conn.execute(f"DROP TABLE {table_name}")

# close the connection
conn.close()