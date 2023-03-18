import urllib.request
import urllib.parse


url = 'https://westworld.fandom.com/wiki/Westworld_Wiki'
f = urllib.request.urlopen(url)
contents = f.read().decode('utf-8')

f = open('fandom.html', 'wb')
f.write(contents.encode('utf-8'))
f.close()