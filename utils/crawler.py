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

#=====douban=====
def get_douban_bookinfo(ISBN):
	#browser = webdriver.PhantomJS(service_log_path=LOG_DIR +'/ghostdriver.log')
	browser = webdriver.Firefox(firefox_options=options, log_path=LOG_DIR +'/ghostdriver.log')

	url = u'https://book.douban.com/subject_search'
	values = {}
	values['search_text'] = ISBN.encode('utf-8')
	data = urllib.urlencode(values) 
	url = url + "?"+data
	browser.get(url)

	soup = BeautifulSoup(browser.page_source, 'html5lib')
	browser.quit()

	url_list = [i['href'] for i in soup.find_all("a", class_="title-text")]

	for url in url_list:
		session = requests.Session()
		response = session.get(url)
		response.encoding = 'utf-8'
		res = response.text
		soup = BeautifulSoup(res, 'html5lib')
		pattern = re.compile(ur'ISBN')
		item = soup.find("span", text=pattern)
		get_ISBN = unicode(item.next_sibling.string).replace(' ', '').replace('\n', '')
		if get_ISBN == ISBN:
			break

	bookname_soup = soup.find('span', property="v:itemreviewed")
	bookname = unicode(bookname_soup.string)

	info = soup.find("div", id='info')
	item = info.find_all('span')

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

	pattern = re.compile(ur'装帧')
	item = soup.find("span", text=pattern)
	bookbinding = unicode(item.next_sibling.string).replace(' ', '').replace('\n', '')

	return {
		'ISBN': get_ISBN,
		'bookname': bookname,
		'author': author,
		'house': house,
		'date': date,
		'bookbinding' :bookbinding,
		'chinese_book_category': '',
		'order': '',
	}

def get_douban_bookinfo_list(query_text):
	#browser = webdriver.PhantomJS(service_log_path=LOG_DIR +'/ghostdriver.log')
	browser = webdriver.Firefox(firefox_options=options, log_path=LOG_DIR +'/ghostdriver.log')

	url = u'https://book.douban.com/subject_search'
	values = {}
	values['search_text'] = query_text.encode('utf-8')
	data = urllib.urlencode(values) 
	url = url + "?"+data
	browser.get(url)

	soup = BeautifulSoup(browser.page_source, 'html5lib')
	browser.quit()

	url_list = [i['href'] for i in soup.find_all("a", class_="title-text")]
	bookinfo_list = []
	for url in url_list:
		session = requests.Session()
		response = session.get(url)
		response.encoding = 'utf-8'
		res = response.text
		soup = BeautifulSoup(res, 'html5lib')
		info = soup.find("div", id='info')
		item = info.find_all('span')

		try:
			pattern = re.compile(ur'ISBN')
			item = soup.find("span", text=pattern)
			get_ISBN = unicode(item.next_sibling.string).replace(' ', '').replace('\n', '')

			#==========
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
			#==========
		except BaseException as e:
			continue

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
	url = 'http://isbn.ncl.edu.tw/NCL_ISBNNet/H30_SearchBooks.php'
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

	url = 'http://isbn.ncl.edu.tw/NCL_ISBNNet/main_DisplayResults.php?PHPSESSID=' +phpsessid +'&Pact=DisplayAll'
#	url = 'http://isbn.ncl.edu.tw/NCL_ISBNNet/main_DisplayRecord.php?PHPSESSID=' +phpsessid +'&Pact=DisplayAll'
	response = session.get(url)
	response.encoding = 'utf-8'
	res = response.text
	soup = BeautifulSoup(res, 'html5lib')
	data_tags = soup.find_all('td', class_=u'資料列_1')

	pattern = re.compile(ur'找到 (\d{1,}) 筆')
	record_count = pattern.search(res).group(1)
	record_count = int(record_count)

	for i in range(record_count):
		url = 'http://isbn.ncl.edu.tw/NCL_ISBNNet/main_DisplayRecord.php?PHPSESSID=' +phpsessid +'&Pact=init&Pstart=' +str(i+1)
		response = session.get(url)
		response.encoding = 'utf-8'
		res = response.text
		soup = BeautifulSoup(res, 'html5lib')
		data_tags = soup.find_all('td', class_=u'資料列_1')
		advance_info = data_tags[14:]

		for j in range(len(advance_info)):
			get_ISBN = unicode(advance_info[j*7 +0].string).replace(u' ', '')
			pattern = re.compile(r'(\d{13,13}).*')
			try:
				get_ISBN = pattern.search(get_ISBN).group(1)
			except:
				get_ISBN = ''
			if not get_ISBN == ISBN:
				continue

			bookname = unicode(data_tags[1].string).replace(u' ', '')
			author = unicode(data_tags[3].string).replace(u' ', '')
			house = unicode(data_tags[5].string).replace(u' ', '')
			date = unicode(advance_info[j*7 +4].string).replace(u' ', '')
			year = int(date.split('/')[0]) +1911
			month = int(date.split('/')[1])
			date = unicode(datetime.date(year,month,1))

			try:
				bookbinding = unicode(advance_info[j*7 +0].string).replace(u' ', '')
				pattern = re.compile(r'\((.*)\)')
				bookbinding = pattern.search(bookbinding).group(1)
			except BaseException as e:
				bookbinding = ''
			try:
				chinese_book_category = unicode(data_tags[9].string).replace(u' ', '')
				pattern = re.compile(r'(\d{3,3}).*')
				chinese_book_category = pattern.search(chinese_book_category).group(1)
			except BaseException as e:
				chinese_book_category = ''
			try:
				order = unicode(data_tags[7].string).replace(u' ', '')
			except BaseException as e:
				order = ''
			return {
				'ISBN': get_ISBN,
				'bookname': bookname,
				'author': author,
				'house': house,
				'date': date,
				'bookbinding' :bookbinding,
				'chinese_book_category': chinese_book_category,
				'order': order,
			}

	return {}

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
#	url = 'http://isbn.ncl.edu.tw/NCL_ISBNNet/main_DisplayRecord.php?PHPSESSID=' +phpsessid +'&Pact=DisplayAll'
	response = session.get(url)
	response.encoding = 'utf-8'
	res = response.text
	soup = BeautifulSoup(res, 'html5lib')
	data_tags = soup.find_all('td', class_=u'資料列_1')

	pattern = re.compile(ur'找到 (\d{1,}) 筆')
	record_count = pattern.search(res).group(1)
	record_count = int(record_count)
	if record_count > 100:
		raise SystemError(u'查詢回傳大量資料，請縮小查詢範圍')

	bookinfo_list = []
	for i in range(record_count):
		url = 'http://isbn.ncl.edu.tw/NCL_ISBNNet/main_DisplayRecord.php?PHPSESSID=' +phpsessid +'&Pact=init&Pstart=' +str(i+1)
		response = session.get(url)
		response.encoding = 'utf-8'
		res = response.text
		soup = BeautifulSoup(res, 'html5lib')
		data_tags = soup.find_all('td', class_=u'資料列_1')
		advance_info = data_tags[14:]

		for j in range(len(advance_info)):
			try:
				get_ISBN = unicode(advance_info[7*j +0].string).replace(u' ', '')
				pattern = re.compile(r'(\d{13,13}).*')
				get_ISBN = pattern.search(get_ISBN).group(1)
				bookname = unicode(data_tags[1].string).replace(u' ', '')
				author = unicode(data_tags[3].string).replace(u' ', '')
				house = unicode(data_tags[5].string).replace(u' ', '')
				date = unicode(advance_info[j*7 +4].string).replace(u' ', '')
				year = int(date.split('/')[0]) +1911
				month = int(date.split('/')[1])
				date = unicode(datetime.date(year,month,1))
			except BaseException as e:
				continue

			try:
				bookbinding = unicode(advance_info[j*7 +0].string).replace(u' ', '')
				pattern = re.compile(r'\((.*)\)')
				bookbinding = pattern.search(bookbinding).group(1)
			except BaseException as e:
				bookbinding = ''
			try:
				chinese_book_category = unicode(data_tags[9].string).replace(u' ', '')
				pattern = re.compile(r'(\d{3,3}).*')
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
				'bookbinding': bookbinding,
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
	r = get_ncl_bookinfo(u'9789573321569')
	print(r[1])
	r = get_douban_bookinfo(u'9787801871527')
	print(r[1])
	r_list = get_douban_bookinfo_list(u'天藍色')
	for i in r_list:
		print(i[1])