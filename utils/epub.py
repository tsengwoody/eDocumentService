# coding=utf-8
import io
import os
import shutil
import sys
from bs4 import BeautifulSoup, NavigableString
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

	new_metadata_DC = {}
	for k,v in epubBook.metadata[epub.NAMESPACES['DC']].iteritems():
		for t in v:
			new_metadata_DC[k] = []
			try:
				if not t[1]['id'] == 'eDocumentService':
					new_metadata_DC[k].append(t)
			except:
				new_metadata_DC[k].append(t)
			if new_metadata_DC[k] == []:
				del new_metadata_DC[k]
	epubBook.metadata[epub.NAMESPACES['DC']] = new_metadata_DC

	epubBook.add_metadata('DC', 'title', kwargs['bookname'], {'id': 'eDocumentService'})
	epubBook.add_metadata('DC', 'creator', kwargs['author'], {'id': 'eDocumentService'})
	epubBook.add_metadata('DC', 'ISBN', kwargs['ISBN'], {'id': 'eDocumentService'})
	epubBook.add_metadata('DC', 'date', kwargs['date'], {'id': 'eDocumentService'})
	epubBook.add_metadata('DC', 'publisher', kwargs['house'], {'id': 'eDocumentService'})
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
					print e
				temp_file = temp_folder +'/part{0}.txt'.format(part)
				fw = io.open(temp_file, 'w', encoding='utf-8')
				part_list.append(temp_file)
			fw.write(line)
		fw.close()

	from tag import add_tag, add_template_tag
	for f in part_list:
		add_tag(f, f,)
		add_template_tag(f, f, 'book_template.html')

	html2epub(part_list, dst, **kwargs)

	shutil.rmtree(temp_folder)

if __name__ == '__main__':
	pass