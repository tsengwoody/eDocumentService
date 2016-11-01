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

def add_base_url(src, id, encoding='utf-8'):
#	try:
	import re
	soup = BeautifulSoup(open(src), 'lxml')
	base_url = '/static/article/{0}/'.format(id)
	tags = soup.find_all(src=re.compile('^[\d\w]+'))
	for tag in tags:
		tag['src'] = base_url +tag['src']
		print tag['src']
	with codecs.open(src, 'w', encoding=encoding) as dstFile:
		dst_content = soup.prettify(formatter='html').replace(u'\n', u'\r\n')
		dstFile.write(dst_content)
	return True
#	except:
#		return False

def add_tag(source, destination, encoding='utf-8'):
	with codecs.open(source, 'r', encoding=encoding) as sourceFile:
		source_content = sourceFile.read()
#		source_content = source_content[1:]
	destination_content = '<p>' +source_content.replace('\r\n', '</p>\r\n<p>') +'</p>'
	with codecs.open(destination, 'w', encoding=encoding) as destinationFile:
		destinationFile.write(destination_content)

def add_template_tag(source, destination, template, encoding='utf-8'):
	with codecs.open(template, 'r', encoding=encoding) as templateFile:
		template_content = templateFile.read()
		head = template_content.split('{}')[0][1:]
		tail = template_content.split('{}')[1]
	with codecs.open(source, 'r', encoding=encoding) as sourceFile:
		source_content = sourceFile.read()
#		file_head = source_content[0]
#		source_content = source_content[1:]
	source_content = head +source_content +tail
	with codecs.open(destination, 'w', encoding=encoding) as destinationFile:
		destinationFile.write(source_content)

def clean_tag(source,  destination, title='', encoding='utf-8'):
	with codecs.open(source, 'r', encoding=encoding) as sourceFile:
		source_content = sourceFile.read()
#	file_head = source_content[0]
#	source_content = source_content[1:]
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

import sys
if __name__ == '__main__':
	add_tag(sys.argv[1], sys.argv[2])
	add_template_tag(sys.argv[2], sys.argv[2], 'book_template.html')
	clean_tag(sys.argv[2], sys.argv[2])