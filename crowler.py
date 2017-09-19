import urllib2, urllib, os

seed=raw_input('Enter a url : ')

type = ['jpg', 'png', 'jpeg', 'JPEG']

if not os.path.exists('Imgs'):
	os.mkdir('Imgs')

def google_links(page):

	opener = urllib2.build_opener()
	opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
	response = opener.open(page)
	html = response.read()
	res = []
	links = html.split('href="/url?q=')
	for i in range(len(links)-1):
		temp = links[i+1]
		link = temp.split('&')[0]
		if len(link.split(':')) == 2 and len(link.split('%')) == 1:
			res.append(link)
	return res

def extract(pages):

	for page in pages:

		print 'Page -- ' + page

		opener = urllib2.build_opener()
		opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
		response = opener.open(page)
		html = response.read()
		res = []
		links = html.split('<img src="')
		for i in range(len(links)-3):
			temp = links[i+1]
			link = temp.split('"')[0]
			print 'Link -- ' + link
			file_type = link.split('.')
			if (file_type[len(file_type)-1] in type) and (link[:4] == 'http') :
				if not os.path.exists('Imgs/' + page[12:20]):
					os.mkdir('Imgs/' + page[12:20])
				name =  'Imgs/' +  page[12:20] + '/' + str(i)  + '.jpg'
				urllib.urlretrieve(link, name)

if ('https://' in seed) or ('http://' in seed):
	result = []
	result.append(seed)
	extract(result)
else:
	query = ""
	words = seed.split(' ')
	for word in words:
		query = query + word + '+'
	seed = "https://www.google.co.in/search?safe=off&q=" + query
	result = google_links(seed)
	extract(result)
