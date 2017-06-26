#!/usr/bin/env python

import sys
from ebooklib import epub

def through(src, dst):

	book = epub.read_epub(src)

	'''try:
		del book.metadata['http://purl.org/dc/elements/1.1/']['identifier'][0]
	except:
		pass
	book.set_identifier('eDocumentService')'''

	nav = 0
	for item in book.items:
		if isinstance(item, epub.EpubNav):
			book.items[book.items.index(item)] = epub.EpubNav()
			nav = nav +1

		if not nav:
			book.add_item(epub.EpubNav())

	epub.write_epub(dst, book, {})

if __name__ == '__main__':
	through(sys.argv[1], sys.argv[2])