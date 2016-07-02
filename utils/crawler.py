# coding: utf-8
import requests
import codecs
import urllib,urllib2
import cookielib
import datetime
from bs4 import BeautifulSoup
from mysite.settings import PREFIX_PATH

def load_post_data(source):
	post_data = {}
	with codecs.open(source, 'r', encoding='utf-8') as sFile:
		line = sFile.next()
		line = line[1:]
		line = line.replace('\r\n','')
		lineSplit = line.split('=')
		if len(lineSplit) == 2:
			(key,value) = (lineSplit[0],lineSplit[1])
			key = unicode(key).encode('utf-8')
			value = unicode(value).encode('utf-8')
			post_data[key] = value
		if len(lineSplit) == 1:
			key = lineSplit[0]
			key = unicode(key).encode('utf-8')
			post_data[key] = u''
		for line in sFile:
			line = line.replace('\r\n','')
			lineSplit = line.split('=')
			if len(lineSplit) == 2:
				(key,value) = (lineSplit[0],lineSplit[1])
				key = unicode(key).encode('utf-8')
				value = unicode(value).encode('utf-8')
				post_data[key] = value
			if len(lineSplit) == 1:
				key = lineSplit[0]
				key = unicode(key).encode('utf-8')
				post_data[key] = u''
	return post_data

def get_book_info(ISBN):
	url = 'http://isbn.ncl.edu.tw/NCL_ISBNNet/H30_SearchBooks.php'
	cookie = cookielib.CookieJar()
	handler=urllib2.HTTPCookieProcessor(cookie)
	opener = urllib2.build_opener(handler)
	response = opener.open(url)
	for item in cookie:
		if item.name == 'PHPSESSID':
			phpsessid = item.value
	#		print 'Name = '+item.name
	#		print 'Value = '+item.value
	#url = url +'?PHPSESSID' +'=' +phpsessid
	post_data_file = PREFIX_PATH +'/utils/post_data.txt'
	values = load_post_data(post_data_file)
	values['FO_SearchValue0'] = ISBN
	data = urllib.urlencode(values)  
	user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
	headers = { 'User-Agent' : user_agent }  
	request = urllib2.Request(url, data, headers)  
	response = opener.open(request)
	url = 'http://isbn.ncl.edu.tw/NCL_ISBNNet/main_DisplayResults.php?PHPSESSID=' +phpsessid +'&Pact=DisplayAll'
	response = opener.open(url)
	res = response.read().decode('utf-8')
	soup = BeautifulSoup(res, 'html5lib')
	td = soup.find_all('td', class_=u'資料列_1')
	if not td:
		return [False]
	bookname = unicode(td[4].string)
	author = unicode(td[5].string)
	house = unicode(td[6].string)
	date = unicode(td[7].string)
	year = int(date.split('/')[0]) +1911
	month = int(date.split('/')[1])
	date = unicode(datetime.date(year,month,1))
	return [True, bookname, author, house, date]

if __name__ == '__main__':
	book_info = get_book_info('9789573323969')
	for info in book_info:
		print info