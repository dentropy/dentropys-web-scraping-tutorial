#!/bin/bash
bash ./clear.sh
python3 1_Create_SQLite_Database.py
python3 2_INSERT_URL_We_want_To_Scrape.py
python3 3_Print_SELECT.py
python3 4_Scrape_URL.py
python3 5_Extract_URLs.py 
echo "That's it"
