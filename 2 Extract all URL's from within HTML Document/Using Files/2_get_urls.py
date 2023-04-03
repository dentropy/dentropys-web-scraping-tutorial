from os import path

if (path.isfile('fandom.html') == False):
  print("You need to run `python3 1_scrape_fandom_dit_com.py first`")
  quit()

with open('fandom.html', 'r') as file:
    html_doc = file.read().replace('\n', '')

try:
  from bs4 import BeautifulSoup
except:
  print("You need to run `pip install beautifulsoup4`")
soup = BeautifulSoup(html_doc, 'html.parser')
url_links = []
for link in soup.find_all('a'):
    url_links.append(  link.get('href')  )

import json
with open('urls.json', 'w') as f:
    json.dump(url_links, open('urls.json', 'w'))