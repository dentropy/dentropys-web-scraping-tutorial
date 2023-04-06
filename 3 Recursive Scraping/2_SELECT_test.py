import os
from WebScrapingOrchestration import WebScrapingOrchestration
from pprint import pprint

engine_path = "sqlite+pysqlite:///" + "/".join(os.getcwd().split("/")) + "/scraped_data.db"
wso = WebScrapingOrchestration(engine_path)

result = wso.test_database_connection()
for row in result:
  pprint(row.__dict__)
