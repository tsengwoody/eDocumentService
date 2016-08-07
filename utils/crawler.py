# coding: utf-8
import codecs
import cookielib
import datetime
import re
import urllib,urllib2
from bs4 import BeautifulSoup
from mysite.settings import BASE_DIR

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
	post_data_file = BASE_DIR +'/utils/post_data.txt'
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
	bookname=''
	author=''
	house=''
	date=''
	try:
		bookname = unicode(td[4].string)
		author = unicode(td[5].string)
		house = unicode(td[6].string)
		date = unicode(td[7].string)
		year = int(date.split('/')[0]) +1911
		month = int(date.split('/')[1])
		date = unicode(datetime.date(year,month,1))
		status = u'success'
	except:
		status = u'error'
	return [status, bookname, author, house, date]

def ISBN10_check(ISBN):
	match = re.search(r'^(\d{9})(\d|X)$', ISBN)
	if not match:
		return False
	digits = match.group(1)
	check_digit = 10 if match.group(2) == 'X' else int(match.group(2))
	result = sum((i + 1) * int(digit) for i, digit in enumerate(digits))
	return (result % 11) == check_digit

def ISBN13_check(ISBN):
	match = re.search(r'^(\d{12})(\d)$', ISBN)
	if not match:
		return False
	digits = match.group(1)
	check_digit = int(match.group(2))
	result = sum((3 * int(digit) if i % 2 == 1 else int(digit) for i, digit in enumerate(digits)))
	return ((result + check_digit) % 10) == 0

def ISBN10_to_ISBN13(ISBN):
	match = re.search(r'^(\d{9})(\d|X)$', ISBN)
	if not match:
		return False
	digits = match.group(1)
	digits = '978' +digits
	result = sum((3 * int(digit) if i % 2 == 1 else int(digit) for i, digit in enumerate(digits)))
	check_digit = (10 - (result % 10)) % 10
	return str(digits +str(check_digit))

if __name__ == '__main__':
	book_info = get_book_info('9789573323969')
	for info in book_info:
		print info
	print ISBN10_to_ISBN13('957331990X')
	print ISBN13_check('9789865829810')