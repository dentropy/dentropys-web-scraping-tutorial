import os
from WebScrapingOrchestration import WebScrapingOrchestration
from db import Urls, Scarping_queue, Scraped_urls_logs, Url_contents
engine_path = "sqlite+pysqlite:///" + "/".join(os.getcwd().split("/")) + "/scraped_data.db"
wso = WebScrapingOrchestration(engine_path)

url_to_scrape = "https://gameofthrones.fandom.com/wiki/Game_of_Thrones_Wiki"

# wso.test_database_connection()
# wso.insert_url(url_to_scrape)
# wso.add_url_to_scraping_queue(url_to_scrape)
# wso.scrape_url()
# wso.extract_urls()

wso.recursive_scraping("gameofthrones.fandom.com", 10)