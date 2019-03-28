# coding: utf-8
import codecs
#import cookielib
import datetime
import os
import re
import requests
import urllib
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
options = Options()
options.add_argument("--headless")
LOG_DIR = os.path.dirname(os.path.abspath(__file__))

from threading import Thread, Lock

try:
	from Queue import Queue, Empty
	unicode = unicode
	from urllib import urlencode
except:
	from queue import Queue, Empty
	unicode = str
	from urllib.parse import urlencode

def worker_get_bookinfo_detail(function, urls, result, mutex, session):
	while True:
		try:
			if mutex.acquire():
				item = urls.get(block=False)
		except Empty as e:
			break
		finally:
			mutex.release()

		r = function(item, session)

		if mutex.acquire():
			result.put(r)
			mutex.release()

#=====douban=====
def get_douban_bookinfo(ISBN):
	#browser = webdriver.PhantomJS(service_log_path=LOG_DIR +'/ghostdriver.log')
	browser = webdriver.Firefox(options=options, service_log_path=LOG_DIR +'/ghostdriver.log')

	url = u'https://book.douban.com/subject_search'
	values = {}
	values['search_text'] = ISBN.encode('utf-8')
	data = urlencode(values) 
	url = url + "?"+data
	browser.get(url)

	soup = BeautifulSoup(browser.page_source, 'html5lib')
	browser.quit()

	session = requests.Session()
	url_list = [i['href'] for i in soup.find_all("a", class_="title-text")]

	bookinfo_list = []
	result = Queue()
	urls = Queue()
	for url in url_list:
		urls.put(url)

	threads = []
	mutex = Lock()
	for t in range(8):
		t = Thread(target=worker_get_bookinfo_detail, kwargs={'function':get_douban_bookinfo_detail, 'urls': urls, 'result': result, 'mutex':mutex, 'session': session})
		t.start()
		threads.append(t)
	for t in threads:
		t.join()

	while True:
		try:
			item = result.get(block=False)
		except:
			break
		bookinfo_list.extend(item)

	return bookinfo_list[0]

def get_douban_bookinfo_list(query_text):
	#browser = webdriver.PhantomJS(service_log_path=LOG_DIR +'/ghostdriver.log')
	browser = webdriver.Firefox(options=options, service_log_path=LOG_DIR +'/ghostdriver.log')

	url = u'https://book.douban.com/subject_search'
	values = {}
	values['search_text'] = query_text.encode('utf-8')
	data = urlencode(values) 
	url = url + "?"+data
	browser.get(url)

	soup = BeautifulSoup(browser.page_source, 'html5lib')
	browser.quit()

	session = requests.Session()
	url_list = [i['href'] for i in soup.find_all("a", class_="title-text")]

	bookinfo_list = []
	result = Queue()
	urls = Queue()
	for url in url_list:
		urls.put(url)

	threads = []
	mutex = Lock()
	for t in range(8):
		t = Thread(target=worker_get_bookinfo_detail, kwargs={'function':get_douban_bookinfo_detail, 'urls': urls, 'result': result, 'mutex':mutex, 'session': session})
		t.start()
		threads.append(t)
	for t in threads:
		t.join()

	while True:
		try:
			item = result.get(block=False)
		except:
			break
		bookinfo_list.extend(item)

	return bookinfo_list

def get_douban_bookinfo_detail(url, session):
	bookinfo_list = []

	response = session.get(url)
	response.encoding = 'utf-8'
	res = response.text
	soup = BeautifulSoup(res, 'html5lib')
	#info = soup.find("div", id='info')
	#item = info.find_all('span')

	try:
		pattern = re.compile(ur'ISBN')
		item = soup.find("span", text=pattern)
		get_ISBN = unicode(item.next_sibling.string).replace(' ', '').replace('\n', '')

		bookname_soup = soup.find('span', property="v:itemreviewed")
		bookname = unicode(bookname_soup.string)
		try:
			pattern = re.compile(ur'副标题')
			item = soup.find("span", text=pattern)
			subtitle = unicode(item.next_sibling.string).replace(' ', '').replace('\n', '')
			bookname = u'{0}, {1}'.format(bookname, subtitle)
		except:
			pass
		try:
			pattern = re.compile(ur'原作名')
			item = soup.find("span", text=pattern)
			orgtitle = unicode(item.next_sibling.string).replace(' ', '').replace('\n', '')
			bookname = u'{0}; {1}'.format(bookname, orgtitle)
		except:
			pass
		pattern = re.compile(ur'作者')
		item = soup.find("span", text=pattern)
		author = unicode(item.next_sibling.next_sibling.string).replace(' ', '').replace('\n', '')
		try:
			pattern = re.compile(ur'译者')
			item = soup.find("span", text=pattern)
			translator = unicode(item.next_sibling.next_sibling.string).replace(' ', '').replace('\n', '')
			author = u'{0}作; {1}译'.format(author, translator)
		except:
			pass
		pattern = re.compile(ur'出版社')
		item = soup.find("span", text=pattern)
		house = unicode(item.next_sibling.string).replace(' ', '').replace('\n', '')
		pattern = re.compile(ur'出版年')
		item = soup.find("span", text=pattern)
		date = unicode(item.next_sibling.string).replace(' ', '').replace('\n', '')
		year = int(date.split('-')[0])
		month = int(date.split('-')[1])
		date = unicode(datetime.date(year,month,1))
	except BaseException as e:
		return []
	try:
		pattern = re.compile(ur'装帧')
		item = soup.find("span", text=pattern)
		bookbinding = unicode(item.next_sibling.string).replace(' ', '').replace('\n', '')
	except BaseException as e:
		bookbinding = ''
	bookinfo_list.append({
		'ISBN': get_ISBN,
		'bookname': bookname,
		'author': author,
		'house': house,
		'date': date,
		'bookbinding': bookbinding,
		'chinese_book_category': '',
		'order': '',
	})

	return bookinfo_list

#=====NCL=====

def load_post_data(src):
	'''import pkgutil
	data = pkgutil.get_data(__package__, src)
	data = data.decode('utf-8')[1:]'''
	src = os.path.join(os.path.dirname(os.path.abspath(__file__)), src)
	with codecs.open(src, encoding='utf-8') as f:
		data = f.read()
	post_data = {}
	for line in data.split('\r\n'):
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

def get_ncl_bookinfo(ISBN):
	url = 'http://isbn.ncl.edu.tw/NEW_ISBNNet/main_DisplayResults.php?&Pact=DisplayAll'
	session = requests.Session()
	response = session.get(url)
	cookies_dict = session.cookies.get_dict()
	for key in cookies_dict:
		if key == 'PHPSESSID':
			phpsessid = cookies_dict[key]
	post_data_file = 'post_data.txt'
	values = load_post_data(post_data_file)
	values['FO_SearchField0'] = 'ISBN'
	values['FO_SearchValue0'] = ISBN
	response = session.post(url,data=values)

	url = 'http://isbn.ncl.edu.tw/NEW_ISBNNet/main_DisplayResults.php?&Pact=init'
	response = session.get(url)
	url = 'http://isbn.ncl.edu.tw/NEW_ISBNNet/main_DisplayResults.php?&Pact=DisplayAll'
	response = session.get(url)
	response.encoding = 'utf-8'
	res = response.text
	import io
	with io.open('w2.html', 'w', encoding='utf8') as f:
		f.write(res)

	soup = BeautifulSoup(res, 'html5lib')
	data_tags = soup.find_all('td', class_=u'資料列_1')

	pattern = re.compile(ur'找到 (\d{1,}) 筆')
	record_count = pattern.search(res).group(1)
	record_count = int(record_count)
	print(record_count)

	bookinfo_list = []
	result = Queue()
	urls = Queue()
	for i in range(record_count):
		url = 'http://isbn.ncl.edu.tw/NEW_ISBNNet/main_DisplayRecord.php?&Pact=Display&Pstart=' +str(i+1)
		response = session.get(url)
		response.encoding = 'utf-8'
		res = response.text
		soup = BeautifulSoup(res, 'html5lib')
		data_tags = soup.find_all('td', class_=u'資料列_1')
		advance_info = data_tags[14:]
		print(advance_info)
		urls.put(url)

	threads = []
	mutex = Lock()
	for t in range(8):
		t = Thread(target=worker_get_bookinfo_detail, kwargs={'function':get_ncl_bookinfo_detail, 'urls': urls, 'result': result, 'mutex':mutex, 'session': session})
		t.start()
		threads.append(t)
	for t in threads:
		t.join()

	while True:
		try:
			item = result.get(block=False)
		except:
			break
		bookinfo_list.extend(item)

	return bookinfo_list[0]

def get_ncl_bookinfo_list(query_dict):
	url = 'http://isbn.ncl.edu.tw/NCL_ISBNNet/H30_SearchBooks.php'
	session = requests.Session()
	response = session.get(url)
	cookies_dict = session.cookies.get_dict()
	for key in cookies_dict:
		if key == 'PHPSESSID':
			phpsessid = cookies_dict[key]
	post_data_file = 'post_data.txt'
	values = load_post_data(post_data_file)
	values.update(query_dict)
	response = session.post(url,data=values)

	url = 'http://isbn.ncl.edu.tw/NCL_ISBNNet/main_DisplayResults.php?PHPSESSID=' +phpsessid +'&Pact=DisplayAll'
	#url = 'http://isbn.ncl.edu.tw/NCL_ISBNNet/main_DisplayRecord.php?PHPSESSID=' +phpsessid +'&Pact=DisplayAll'
	response = session.get(url)
	response.encoding = 'utf-8'
	res = response.text
	soup = BeautifulSoup(res, 'html5lib')
	data_tags = soup.find_all('td', class_=u'資料列_1')

	pattern = re.compile(ur'找到 (\d{1,}) 筆')
	record_count = pattern.search(res).group(1)
	record_count = int(record_count)

	bookinfo_list = []
	result = Queue()
	urls = Queue()
	for i in range(record_count):
		url = 'http://isbn.ncl.edu.tw/NCL_ISBNNet/main_DisplayRecord.php?PHPSESSID=' +phpsessid +'&Pact=init&Pstart=' +str(i+1)
		urls.put(url)

	threads = []
	mutex = Lock()
	for t in range(8):
		t = Thread(target=worker_get_bookinfo_detail, kwargs={'function':get_ncl_bookinfo_detail, 'urls': urls, 'result': result, 'mutex':mutex, 'session': session})
		t.start()
		threads.append(t)
	for t in threads:
		t.join()

	while True:
		try:
			item = result.get(block=False)
		except:
			break
		bookinfo_list.extend(item)

	return bookinfo_list

def get_ncl_bookinfo_detail(url, session):
	bookinfo_list = []
	print(url)
	response = session.get(url)
	response.encoding = 'utf-8'
	res = response.text
	soup = BeautifulSoup(res, 'html5lib')
	data_tags = soup.find_all('td', class_=u'資料列_1')
	advance_info = data_tags[14:]
	import io
	with io.open('w.html', 'w', encoding='utf8') as f:
		f.write(res)

	for j in range(len(advance_info)):
		try:
			get_ISBN = unicode(advance_info[j*7 +0].string).replace(u' ', '')
			pattern = re.compile(ur'(\d{13,13}).*')
			get_ISBN = pattern.search(get_ISBN).group(1)
			bookname = unicode(data_tags[1].string).replace(u' ', '')
			author = unicode(data_tags[3].string).replace(u' ', '')
			house = unicode(data_tags[5].string).replace(u' ', '')
			date = unicode(advance_info[j*7 +4].string).replace(u' ', '')
			year = int(date.split('/')[0]) +1911
			month = int(date.split('/')[1])
			date = unicode(datetime.date(year,month,1))
		except:
			continue

		try:
			bookbinding = unicode(advance_info[j*7 +0].string).replace(u' ', '')
			pattern = re.compile(ur'\((.*)\)')
			bookbinding = pattern.search(bookbinding).group(1)
		except BaseException as e:
			bookbinding = ''
		try:
			chinese_book_category = unicode(data_tags[9].string).replace(u' ', '')
			pattern = re.compile(ur'(\d{3,3}).*')
			chinese_book_category = pattern.search(chinese_book_category).group(1)
		except BaseException as e:
			chinese_book_category = ''
		try:
			order = unicode(data_tags[7].string).replace(u' ', '')
		except BaseException as e:
			order = ''

		bookinfo_list.append({
			'ISBN': get_ISBN,
			'bookname': bookname,
			'author': author,
			'house': house,
			'date': date,
			'bookbinding' :bookbinding,
			'chinese_book_category': chinese_book_category,
			'order': order,
		})

	return bookinfo_list

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
	import time
	'''s = time.time()
	r = get_ncl_bookinfo(u'9789573321569')
	e = time.time()
	print(r['bookname'])
	print(e-s)

	s = time.time()
	r = get_ncl_bookinfo_list({
		'FO_SearchValue0' :u'零之使魔',
		'FO_SearchField0': 'Title',
	})
	e = time.time()
	print(e-s)
	print(r[0]['bookname'])'''

	s = time.time()
	r = get_douban_bookinfo(u'9787801871527')
	e = time.time()
	print(e-s)
	print(r['bookname'])

	s = time.time()
	r_list = get_douban_bookinfo_list(u'天藍色')
	e = time.time()
	print(e-s)
	print(len(r))