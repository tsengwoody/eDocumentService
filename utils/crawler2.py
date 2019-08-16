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
from selenium.webdriver.support.ui import Select
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

def kill_firefox():
	import subprocess
	p=subprocess.Popen("killall firefox", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(stdoutput,erroutput) = p.communicate()

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
	kill_firefox()

	session = requests.Session()
	url_list = [i['href'] for i in soup.find_all("a", class_="title-text")]

	bookinfo_list = []
	for url in url_list:
		item = get_douban_bookinfo_detail(url, session)
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
	kill_firefox()

	session = requests.Session()
	url_list = [i['href'] for i in soup.find_all("a", class_="title-text")]

	bookinfo_list = []
	for url in url_list:
		item = get_douban_bookinfo_detail(url, session)
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

FO_SearchField2Index = {
	'Title': 0,
	'Author': 1,
	'PublisherShortTitle': 2,
	'SubjHeading': 3,
	'SerialTitle': 4,
	'ClassNo': 5,
	'ISBN': 6,
	'Date_Sales': 7,
	'PubMonth_Pre': 8,
}

FO_SchRe1ation2Index = {
	'AND': 0,
	'OR': 1,
	'NOT': 2,
}

def get_ncl_bookinfo(ISBN):
	browser = webdriver.Firefox(options=options, service_log_path=LOG_DIR +'/ghostdriver.log')
	url = 'http://isbn.ncl.edu.tw/NEW_ISBNNet/H30_SearchBooks.php'
	browser.get(url)
	select0 = Select(browser.find_element_by_name('FO_SearchField0'))
	select0.select_by_index(FO_SearchField2Index['ISBN'])
	input0 = browser.find_element_by_name('FO_SearchValue0')
	input0.send_keys(ISBN)
	search = browser.find_element_by_link_text('開始查詢')
	search.click()

	result_url = browser.current_url
	result_page = browser.page_source

	pattern = re.compile(ur'找到 (\d{1,}) 筆')
	record_count = pattern.search(result_page).group(1)
	record_count = int(record_count)

	bookinfo_list = []
	detail_urls = []
	for i in range(1):
		result_table = browser.find_element_by_class_name('table-searchbooks')
		books_link = result_table.find_elements_by_tag_name('a')
		detail_urls.append(books_link[i].get_attribute('href'))
	for detail_url in detail_urls:
		browser.get(detail_url)
		book_page = browser.page_source
		item = get_ncl_bookinfo_detail(book_page)
		bookinfo_list.extend(item)

	browser.quit()
	kill_firefox()

	return bookinfo_list[0]

def get_ncl_bookinfo_list(query_dict):
	browser = webdriver.Firefox(options=options, service_log_path=LOG_DIR +'/ghostdriver.log')
	url = 'http://isbn.ncl.edu.tw/NEW_ISBNNet/H30_SearchBooks.php'
	browser.get(url)
	select0 = Select(browser.find_element_by_name('FO_SearchField0'))
	select0.select_by_index(FO_SearchField2Index[query_dict['FO_SearchField0']])
	input0 = browser.find_element_by_name('FO_SearchValue0')
	input0.send_keys(query_dict['FO_SearchValue0'])

	conjunction1 = Select(browser.find_element_by_name('FO_SchRe1ation1'))
	conjunction1.select_by_index(FO_SchRe1ation2Index[query_dict['FO_SchRe1ation1']])
	select1 = Select(browser.find_element_by_name('FO_SearchField1'))
	select1.select_by_index(FO_SearchField2Index[query_dict['FO_SearchField1']])
	input1 = browser.find_element_by_name('FO_SearchValue1')
	input1.send_keys(query_dict['FO_SearchValue1'])

	conjunction2 = Select(browser.find_element_by_name('FO_SchRe1ation2'))
	conjunction2.select_by_index(FO_SchRe1ation2Index[query_dict['FO_SchRe1ation2']])
	select2 = Select(browser.find_element_by_name('FO_SearchField2'))
	select2.select_by_index(FO_SearchField2Index[query_dict['FO_SearchField2']])
	input2 = browser.find_element_by_name('FO_SearchValue2')
	input2.send_keys(query_dict['FO_SearchValue2'])

	search = browser.find_element_by_link_text('開始查詢')
	search.click()

	result_url = browser.current_url
	result_page = browser.page_source

	pattern = re.compile(ur'找到 (\d{1,}) 筆')
	record_count = pattern.search(result_page).group(1)
	record_count = int(record_count)

	bookinfo_list = []
	detail_urls = []
	for i in range(1):
		result_table = browser.find_element_by_class_name('table-searchbooks')
		books_link = result_table.find_elements_by_tag_name('a')
		detail_urls.append(books_link[i].get_attribute('href'))
	for detail_url in detail_urls:
		browser.get(detail_url)
		book_page = browser.page_source
		item = get_ncl_bookinfo_detail(book_page)
		bookinfo_list.extend(item)

	browser.quit()
	kill_firefox()

	return bookinfo_list

def get_ncl_bookinfo_detail(res):
	bookinfo_list = []
	soup = BeautifulSoup(res, 'html5lib')
	data_tags = soup.find(class_=u'table-bookinforight').find_all('td')
	advance_info = soup.find(class_=u'table-bookinfo').find_all('td')

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
	s = time.time()
	r = get_ncl_bookinfo(u'9789573321569')
	e = time.time()
	print(r['bookname'])
	print(e-s)

	s = time.time()
	r = get_ncl_bookinfo_list({
		'FO_SearchValue0' :u'零之使魔',
		'FO_SearchField0': 'Title',
		'FO_SchRe1ation1': 'OR',
		'FO_SearchValue1' : u'',
		'FO_SearchField1': 'Author',
		'FO_SchRe1ation2': 'OR',
		'FO_SearchValue2' : u'',
		'FO_SearchField2': 'ISBN',
	})
	e = time.time()
	print(e-s)
	print(r[0]['bookname'])

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