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
#		for tag_child in tag.contents:
#			merge_NavigableString(tag_child)

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
		span_tag.unwrap()
	div_tags = soup.find_all('div')
	for div_tag in div_tags:
		div_tag.name = 'p'
	p_tags = soup.find_all('p')
	for p_tag in p_tags:
		del p_tag['class']
	merge_NavigableString(soup)
	soup.head.title.string = title
	with codecs.open( destination, 'w', encoding=encoding) as cleanFile:
		clean_content = soup.prettify(formatter='html').replace(u'\n', u'\r\n')
		soup = BeautifulSoup(clean_content, 'lxml')
		clean_content = soup.prettify(formatter='html').replace(u'\n', u'\r\n')
		cleanFile.write(clean_content)

import sys
if __name__ == '__main__':
#	add_tag(sys.argv[1], sys.argv[2])
	add_template_tag(sys.argv[1], sys.argv[2], 'book_template.html')
	clean_tag(sys.argv[2], sys.argv[2])