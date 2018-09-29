# coding: utf-8
import codecs
import os
from bs4 import BeautifulSoup, NavigableString

def replace(src, encoding='utf-8'):
	with codecs.open(src, 'r', encoding=encoding) as file:
		content = file.read()
	content = content.replace(u'「', u'S「')
	content = content.replace(u'」', u'E」')
	content = content.replace(u'『', u'S『')
	content = content.replace(u'』', u'E』')
	content = content.replace(u'！', u'G！')
	with codecs.open(src, 'w', encoding=encoding) as file:
		file.write(content)

def unreplace(src, encoding='utf-8'):
	with codecs.open(src, 'r', encoding=encoding) as file:
		content = file.read()
	content = content.replace(u'S「', u'「')
	content = content.replace(u'E」', u'」')
	content = content.replace(u'S『', u'『')
	content = content.replace(u'E』', u'』')
	content = content.replace(u'G！', u'！')
	with codecs.open(src, 'w', encoding=encoding) as file:
		file.write(content)

import sys
if __name__ == '__main__':
	replace(sys.argv[1])