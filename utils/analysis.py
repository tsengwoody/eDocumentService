# coding: utf-8
import codecs
import re
from difflib import *
from bs4 import BeautifulSoup, NavigableString
import Levenshtein

def diff(src, dst, encoding='utf-8'):
	with codecs.open(src, 'r', encoding=encoding) as srcFile:
		src_content = srcFile.read()
	src_content = '<p>' +src_content.replace('\r\n', '</p>\r\n<p>') +'</p>'
	srcSoup = BeautifulSoup(src_content, 'lxml')
	src_content_text = srcSoup.get_text().replace('\n', '').replace('\r', '').replace('   ', '').replace('  ', '').replace(u' ', '')
	with codecs.open(dst, 'r', encoding=encoding) as dstFile:
		dst_content = dstFile.read()
	dstSoup = BeautifulSoup(dst_content, 'lxml')
	dst_content_text = dstSoup.get_text().replace('\n', '').replace('\r', '').replace('   ', '').replace('  ', '').replace(u' ', '')
	match = SequenceMatcher(None, src_content_text, dst_content_text).get_matching_blocks()
	same_character = 0
#	for i in range(len(match)):
#		same_character = same_character +match[i].size
	for block in match:
		same_character = same_character +block.size
	return [same_character, len(src_content_text), len(dst_content_text)]

def edit_distance(src, dst, encoding='utf-8'):
	with codecs.open(src, 'r', encoding=encoding) as srcFile:
		src_content = srcFile.read()
	src_content = '<p>' +src_content.replace('\r\n', '</p>\r\n<p>') +'</p>'
	srcSoup = BeautifulSoup(src_content, 'lxml')
	src_content_text = srcSoup.get_text().replace('\n', '').replace('\r', '').replace('   ', '').replace('  ', '').replace(u' ', '')
	with codecs.open(dst, 'r', encoding=encoding) as dstFile:
		dst_content = dstFile.read()
	dstSoup = BeautifulSoup(dst_content, 'lxml')
	dst_content_text = dstSoup.get_text().replace('\n', '').replace('\r', '').replace('   ', '').replace('  ', '').replace(u' ', '')
	return Levenshtein.distance(src_content_text, dst_content_text)

def last_character(src):
	soup = BeautifulSoup(open(src), 'lxml')
	lc_dict = {}
	for tag in soup.body.contents:
		if tag.name == 'p':
			try:
				lc = list(tag.strings)[-1].replace(' ', '').replace('\r', '').replace('\n', '')[-1]
				if not lc in lc_dict.keys():
					lc_dict[lc] = [0, []]
				lc_dict[lc][0] = lc_dict[lc][0] +1
				lc_dict[lc][1].append(tag['id'])
			except:
				pass
	return lc_dict

if __name__ == '__main__':
	import sys
	print edit_distance(sys.argv[1], sys.argv[2])
	print diff(sys.argv[1], sys.argv[2])
#	lc_dict = last_character(sys.argv[3])
#	i=0
#	for key in lc_dict.keys():
#		if lc_dict[key][0] <6:
#			print key +':' +str(lc_dict[key])
#			i=i+1
#	print i