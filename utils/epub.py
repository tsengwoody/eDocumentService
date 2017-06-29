# coding=utf-8

import sys
from ebooklib import epub

def through(src, dst):

	book = epub.read_epub(src)
	#book.set_identifier('eDocumentService')

	nav = 0
	for item in book.items:
		if isinstance(item, epub.EpubNav):
			book.items[book.items.index(item)] = epub.EpubNav()
			nav = nav +1
	if not nav:
		book.add_item(epub.EpubNav())

	epub.write_epub(dst, book, {})

def add_bookinfo(epubBook, **kwargs):
	epubBook.add_metadata('DC', 'title', kwargs['bookname'], {'id': 'eDocumentService'})
	epubBook.add_metadata('DC', 'creator', kwargs['author'], {'id': 'eDocumentService'})
	epubBook.add_metadata('DC', 'ISBN', kwargs['ISBN'], {'id': 'eDocumentService'})
	epubBook.add_metadata('DC', 'date', kwargs['date'], {'id': 'eDocumentService'})
	epubBook.add_metadata('DC', 'publisher', kwargs['house'], {'id': 'eDocumentService'})
	return epubBook

from bs4 import BeautifulSoup, NavigableString

def html2epub(part_list, **kwargs):

	book = epub.EpubBook()
	book = add_bookinfo(book, **kwargs)

	c_list = []
	toc = []
	for i in range(len(part_list)):
		c_soup = BeautifulSoup(open(part_list[i]), 'html5lib')
		c = epub.EpubHtml(
			title=u'{0}-part{1}'.format(kwargs['bookname'], i+1),
			file_name='Text/part{0}.xhtml'.format(i+1),
		)
		c.content = c_soup.prettify(formatter="html")
		book.add_item(c)
		c_list.append(c)
		toc.append(
			epub.Link(
				'Text/part{0}.xhtml'.format(i+1),
				'part{0}'.format(i+1),
				'part{0}'.format(i+1),
			)
		)

	book.toc = toc

	book.add_item(epub.EpubNcx())
	book.add_item(epub.EpubNav())
	book.spine = ['nav'] +c_list

	epub.write_epub('{0}.epub'.format(kwargs['ISBN']), book, {})

def txt2epub(part_list, **kwargs):

	book = epub.EpubBook()
	book = add_bookinfo(book, **kwargs)

	c_list = []
	toc = []
	for i in range(len(part_list)):
		c_soup = BeautifulSoup(open(part_list[i]), 'html5lib')
		c = epub.EpubHtml(
			title=u'{0}-part{1}'.format(kwargs['bookname'], i+1),
			file_name='Text/part{0}.xhtml'.format(i+1),
		)
		c.content = c_soup.prettify(formatter="html")
		book.add_item(c)
		c_list.append(c)
		toc.append(
			epub.Link(
				'Text/part{0}.xhtml'.format(i+1),
				'part{0}'.format(i+1),
				'part{0}'.format(i+1),
			)
		)

	book.toc = toc

	book.add_item(epub.EpubNcx())
	book.add_item(epub.EpubNav())
	book.spine = ['nav'] +c_list

	epub.write_epub('{0}.epub'.format(kwargs['ISBN']), book, {})

if __name__ == '__main__':
	html2epub(sys.argv[1], sys.argv[2])
	through(sys.argv[1], sys.argv[1])