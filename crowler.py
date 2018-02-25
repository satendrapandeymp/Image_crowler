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
	time.sleep(1)
	for _ in range(5):
	    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	    time.sleep(1)
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

			name = link.split("://")[1].split("/")[0]
			name = name + "_" + str(random.randint(1,999)) + "." + link.split(".")[-1]
			temp = {"link":link, "name":name, "original":original}
			res.append(temp)
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
		link = doc["link"]
		link = cleanupString(link)
		file_name = name + "/" + doc["name"]
		try:
			test = opener.open(link)
			with open(file_name, 'wb') as file:
				file.write(test.read())
		except:
			print link, doc["original"]
		if count > num:
			break

seed=raw_input('Enter the keywords : ')
num=int(raw_input('No of Images you want -- : '))

query = "https://www.google.co.in/search?client=ubuntu&hs=JQU&channel=fs&dcr=0&source=lnms&tbm=isch&sa=X&ved=0ahUKEwi4hammhsDZAhXBL48KHVVRDtsQ_AUICygC&biw=1366&bih=662" + "+".join(seed.split(' '))
result = google_links(query)
print len(result)
download(seed, result,num)
