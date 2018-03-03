import urllib2, urllib, os, random, cookielib, time, sys, ssl, HTMLParser
from bs4 import BeautifulSoup as Soup
from selenium import webdriver

reload(sys)
sys.setdefaultencoding("utf-8")

def cleanupString(string):
	string = urllib2.unquote(string).decode('utf8')
	return HTMLParser.HTMLParser().unescape(string).encode(sys.getfilesystemencoding())

#type = ['jpg', 'png', 'jpeg', 'JPEG']
if not os.path.exists('Imgs'):
	os.mkdir('Imgs')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0', 'Connection': 'keep-alive',}

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPSHandler(context=ctx), urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [headers]


for key in headers:
    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = headers[key]
browser = webdriver.PhantomJS()

def google_links(page):
	res = []
	browser.get(page)
	time.sleep(2)
	for _ in range(5):
	    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	    time.sleep(2)
	Page_Html = browser.page_source

	Parsed_html = Soup(Page_Html, "html.parser")
	Container = Parsed_html.findAll("div", {"data-async-rclass":"search"})[0]
	rows = Container.findAll("div", {"jscontroller":"Q7Rsec"})

	for row in rows:
		try:
			link = row.findAll("a")[0]['href'].split('&')[0].split("imgurl=")[1]
			original = link
			link = link.replace("%3A", ":")
			link = link.replace("%2F", "/")
			link = link.replace("%2520", "%20")
			res.append(link)
		except:
			print "Found something not captured"

	return res

def download(name, arr, num):
	count = 0
	name = "Imgs/" + name
	if not os.path.exists(name):
		os.mkdir(name)

	for doc in arr:
		count += 1
		link = doc
		link = cleanupString(link)
		link = link.replace(" ", "%20")
		filename = link.split("://")[1].split("/")[0]
		filename = filename + "_" + str(random.randint(1,999)) + "." + link.split(".")[-1].split("%")[0]
		file_name = name + "/" + filename
		try:
			test = opener.open(link, timeout=5)
			with open(file_name, 'wb') as file:
				file.write(test.read())
		except:
			print link
		if count > num:
			break

check =raw_input('Do you have urls.txt ? y/n : ')

if check.lower() == 'y':
	seed=raw_input('Meks sure your filename is in this format -: \nurl1\nurl2\n...\nEnter PATH to Filename : ')
	file = open(seed, 'r')
	result = file.read().split('\n')
	num = len(result)
	seed = seed.split(".")[0]

else:
	seed=raw_input('Enter the keywords : ')
	num=int(raw_input('No of Images you want -- : '))
	query = "https://www.google.com/search?tbm=isch&source=hp&biw=1366&bih=662&ei=qIOSWuyqNMH-vASAs43YDg&gs_l=img.3.0.35i39k1l2j0l8.12015.13207.0.14351.9.9.0.0.0.0.152.847.0j6.6.0....0...1ac.1.64.img..3.6.843.0...0._9c6L5S5nY0&q=" + "+".join(seed.split(' '))
	result = google_links(query)

	with open(seed+".txt", 'wb') as writer:
		for url in result:
			writer.write(url + "\n")

download(seed, result,num)

os.remove("ghostdriver.log")
