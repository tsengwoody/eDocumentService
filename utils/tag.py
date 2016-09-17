# coding: utf-8
import codecs
import os
from bs4 import BeautifulSoup, NavigableString

def merge_NavigableString(tag):
	if isinstance(tag, NavigableString):
		previous_sibling = tag.previous_sibling
		if isinstance(previous_sibling, NavigableString):
			previous_sibling.string.replace_with(previous_sibling.string +tag.string)
			tag.extract()
#			tag.string.replace_with(previous_sibling.string +tag.string)
#			previous_sibling.string.replace_with('*****')
	else:
		for i in xrange(len(tag.contents)-1, -1, -1):
			merge_NavigableString(tag.contents[i])

def add_tag(source, destination, encoding='utf-8'):
	edit_content = ''
	with codecs.open(source, 'r', encoding=encoding) as sourceFile:
		for edit in sourceFile:
			if edit[-2:] == '\r\n':
				edit = '<p>' +edit[:-2] +'</p>' +edit[-2:]
			else:
				edit = '<p>' +edit +'</p>'
			edit_content = edit_content +edit
	edit_content = edit_content[0:3] +edit_content[4:] #skip file head
	if edit_content[-2:] != '\r\n': edit_content=edit_content +'\r\n'
	with codecs.open(destination, 'w', encoding=encoding) as destinationFile:
		destinationFile.write(u'\ufeff' +edit_content)

def add_template_tag(source, destination, template, encoding='utf-8'):
	with codecs.open(template, 'r', encoding=encoding) as templateFile:
		template_content = templateFile.read()
		head = template_content.split('{}')[0][1:]
		tail = template_content.split('{}')[1]
	with codecs.open(source, 'r', encoding=encoding) as sourceFile:
		source_content = sourceFile.read()
		file_head = source_content[0]
		source_content = source_content[1:]
	source_content = head +source_content +tail
	with codecs.open(destination, 'w', encoding=encoding) as destinationFile:
		destinationFile.write(u'\ufeff' +source_content)

def clean_tag(source,  destination, title, encoding='utf-8'):
	with codecs.open(source, 'r', encoding=encoding) as sourceFile:
		source_content = sourceFile.read()
	file_head = source_content[0]
	source_content = source_content[1:]
	source_content = source_content.replace('<br />', '</p>\r\n<p>')
	from bs4 import BeautifulSoup, NavigableString
	soup = BeautifulSoup(source_content, 'lxml')
	span_tags = soup.find_all('span')
	for span_tag in span_tags:
		if not (span_tag.attrs.has_key('class') and ('unknown' in span_tag.attrs['class'] or 'mathml' in span_tag.attrs['class'])):
			span_tag.unwrap()
#		else:
		if span_tag.attrs.has_key('class') and 'unknown' in span_tag.attrs['class']:
			span_tag_string = span_tag.string.split('{???}')
			if len(span_tag_string) == 2:
				span_tag.insert_before(NavigableString(span_tag_string[0]))
				span_tag.string = '{???}'
				span_tag.insert_after(NavigableString(span_tag_string[1]))
	div_tags = soup.find_all('div')
	for div_tag in div_tags:
		div_tag.name = 'p'
	p_tags = soup.find_all('p')
	for p_tag in p_tags:
		del p_tag['class']
	merge_NavigableString(soup)
	soup.head.title.string = title
	for tag in soup.body.contents:
		if isinstance(tag, NavigableString) and tag.string != '\n':
			tag.wrap(soup.new_tag('p'))
	i = 0
	for tag in soup.body.contents:
		if tag.name == 'p':
			tag.attrs['id'] = i
			i = i +1
	with codecs.open( destination, 'w', encoding=encoding) as cleanFile:
		clean_content = soup.prettify(formatter='html').replace(u'\n', u'\r\n')
		soup = BeautifulSoup(clean_content, 'lxml')
		clean_content = soup.prettify(formatter='html').replace(u'\n', u'\r\n')
		cleanFile.write(clean_content)

def find_special_content(source, encoding='utf-8'):
	with codecs.open(source, 'r', encoding=encoding) as sourceFile:
		source_content = sourceFile.read()
	file_head = source_content[0]
	source_content = source_content[1:]
	source_content = source_content.replace('<br />', '</p>\r\n<p>')
	from bs4 import BeautifulSoup, NavigableString
	soup = BeautifulSoup(source_content, 'lxml')
	span_tags = soup.find_all('span')
	for span_tag in span_tags:
		if span_tag.attrs.has_key('class') and ('unknown' in span_tag.attrs['class'] or 'mathml' in span_tag.attrs['class']):
			for parent in span_tag.parents:
				if parent.name == 'p':
					print parent['id']
	img_tags = soup.find_all('img')
	for img_tag in img_tags:
		print img_tag

import sys
if __name__ == '__main__':
#	add_tag(sys.argv[1], sys.argv[1])
#	add_template_tag(sys.argv[1], sys.argv[2], 'book_template.html')
#	clean_tag(sys.argv[2], sys.argv[2])
	find_special_content(sys.argv[1])