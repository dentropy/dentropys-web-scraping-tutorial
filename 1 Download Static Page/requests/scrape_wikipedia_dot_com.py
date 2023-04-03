import urllib.request

url = 'https://wikipedia.com'
f = urllib.request.urlopen(url)
contents = f.read().decode('utf-8')

print(contents)

f = open('wikipedia.html', 'wb')
f.write(contents.encode('utf-8'))
f.close()