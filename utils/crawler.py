# coding: utf-8
import codecs
import cookielib
import datetime
import re
import requests
import urllib,urllib2
from bs4 import BeautifulSoup
#from mysite.settings import BASE_DIR


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
	session = requests.Session()
	response = session.get(url)
	cookies_dict = session.cookies.get_dict()
	for key in cookies_dict:
		if key == 'PHPSESSID':
			phpsessid = cookies_dict[key]
#	post_data_file = BASE_DIR +'/utils/post_data.txt'
	post_data_file = '/django/eDocumentService/utils/post_data.txt'
	values = load_post_data(post_data_file)
	values['FO_SearchValue0'] = ISBN
	response = session.post(url,data=values)
#	url = 'http://isbn.ncl.edu.tw/NCL_ISBNNet/main_DisplayResults.php?PHPSESSID=' +phpsessid +'&Pact=DisplayAll'
	url = 'http://isbn.ncl.edu.tw/NCL_ISBNNet/main_DisplayRecord.php?PHPSESSID=' +phpsessid +'&Pact=DisplayAll'
	response = session.get(url)
	url = 'http://isbn.ncl.edu.tw/NCL_ISBNNet/main_DisplayRecord.php?PHPSESSID=' +phpsessid +'&Pact=init&Pstart=1'
	response = session.get(url)
	response.encoding = 'utf-8'
	res = response.text
	soup = BeautifulSoup(res, 'html5lib')
	data_tags = soup.find_all('td', class_=u'資料列_1')
	try:
		bookname = unicode(data_tags[1].string).replace(u' ', '')
		author = unicode(data_tags[3].string).replace(u' ', '')
		house = unicode(data_tags[5].string).replace(u' ', '')
		date = unicode(data_tags[18].string).replace(u' ', '')
		year = int(date.split('/')[0]) +1911
		month = int(date.split('/')[1])
		date = unicode(datetime.date(year,month,1))
		bookbinding = 	unicode(data_tags[14].string).replace(u' ', '')
		pattern = re.compile(r'\((.*)\)')
		bookbinding = pattern.search(bookbinding).group(1)
		status = u'success'
	except:
		bookname=''
		author=''
		house=''
		date=''
		bookbinding = ''
		status = u'error'
	return [status, bookname, author, house, date, bookbinding]

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

import sys
if __name__ == '__main__':
	book_info = get_book_info(sys.argv[1])
	for info in book_info:
		print info