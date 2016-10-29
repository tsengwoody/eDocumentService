# coding: utf-8
import codecs
import collections
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
	for block in match:
		same_character = same_character +block.size
	return [len(match), same_character, len(src_content_text), len(dst_content_text)]

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
					lc_dict[lc] = []
				lc_dict[lc].append(tag['id'])
			except:
				pass
	return lc_dict

#=====repeat=====

def continue_item(dic, key):
	for i in range(key-3, key+4):
		if not i == key and dic.has_key(i):
			return True
	return False

def find_repeat(src):
	soup = BeautifulSoup(open(src), 'lxml')
	repeat_dict = {}
	p_tags = soup.find_all('p')
	for i,p_tag in enumerate(p_tags):
		before_p_tags = p_tags[0:i]
		for before_p_tag in before_p_tags:
			if same(before_p_tag, p_tag):
				if not repeat_dict.has_key(int(before_p_tag['id'])):
					repeat_dict[int(before_p_tag['id'])] = []
				repeat_dict[int(before_p_tag['id'])].append(int(p_tag['id']))
				break
	repeat_od = collections.OrderedDict(sorted(repeat_dict.items()))
	continue_dict = {}
	for key in repeat_od.keys():
		if continue_item(repeat_od, key):
			continue_dict[key] = repeat_od[key]
	continue_od = collections.OrderedDict(sorted(continue_dict.items()))
	value_sum = []
	for value in repeat_dict.values():
		value_sum = value_sum +value
	duplicate = []
	if not continue_dict == {}:
		for key in range(sorted(continue_dict.keys())[0], sorted(continue_dict.keys())[-1]+1):
			if key in value_sum or key in continue_dict.keys():
				duplicate.append(key)
	return continue_od

def same(src_tag, dst_tag):
	if not (len(src_tag.contents) == len(dst_tag.contents)):
		return False
	tag_len = len(src_tag.contents)
	for i in range(tag_len):
		if not (src_tag.contents[i] == dst_tag.contents[i]):
			return False
	return True

if __name__ == '__main__':
	import sys
	try:
		print edit_distance(sys.argv[1], sys.argv[2])
		print diff(sys.argv[1], sys.argv[2])
		print last_character(sys.argv[3])
		print find_repeat(sys.argv[4])
	except:
		pass