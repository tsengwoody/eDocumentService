#coding=utf-8
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