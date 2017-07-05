# coding=utf-8
import io
import os
import shutil
import sys
from bs4 import BeautifulSoup, NavigableString
from ebooklib import epub

def through(src, dst):

	book = epub.read_epub(src)
	epub.write_epub(dst, book, {})

def add_bookinfo(epubBook, **kwargs):

	for k,v in epubBook.metadata[epub.NAMESPACES['DC']].iteritems():
		if k in kwargs.keys():
			del epubBook.metadata[epub.NAMESPACES['DC']][k]

	epubBook.add_metadata('DC', 'title', kwargs['bookname'])
	epubBook.add_metadata('DC', 'creator', kwargs['author'])
	epubBook.add_metadata('DC', 'source', kwargs['ISBN'])
	epubBook.add_metadata('DC', 'date', kwargs['date'])
	epubBook.add_metadata('DC', 'publisher', kwargs['house'])
	return epubBook

def html2epub(part_list, dst, **kwargs):

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
		c.content = unicode(c_soup)
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

	epub.write_epub(dst, book, {})

def txt2epub(src, dst, line_per_chapter=100, **kwargs):

	temp_folder = 'epub_temp'
	if not os.path.exists(temp_folder):
		os.mkdir(temp_folder)
	part_list = []
	with io.open(src, 'r', encoding='utf-8') as fr:
		for index, line in enumerate(fr.readlines()):
			if index % line_per_chapter == 0:
				part = index/line_per_chapter + 1
				try:
					fw.close()
				except BaseException as e:
					pass
				temp_file = temp_folder +'/part{0}.txt'.format(part)
				fw = io.open(temp_file, 'w', encoding='utf-8')
				part_list.append(temp_file)
			fw.write(line)
		fw.close()

	from tag import add_tag, add_template_tag
	for f in part_list:
		add_tag(f, f,)
		add_template_tag(f, f, )

	html2epub(part_list, dst, **kwargs)

	shutil.rmtree(temp_folder)

if __name__ == '__main__':
	pass