# coding: utf-8
from django.core.management.base import BaseCommand, CommandError

from django.core.cache import cache
from ebookSystem.models import *

class Command(BaseCommand):
	help = 'review part status'
#	def add_arguments(self, parser):
#		parser.add_argument('reviewpart', nargs='*')

	def handle(self, *args, **options):
		BookOrder.objects.all().delete()
		book_list = []
		for book in Book.objects.all():
			if book.status == book.STATUS['active']:
				book_list.append(book)
		try:
			user_order = cache.get(user_order)
		except:
			user_order = []
			for book in book_list:
				if book.owner not in user_order:
					user_order.append(book.owner)
		cache.set('user_order', user_order, 2*86400)

		book_order = []
		while book_list:
			for user in user_order:
				for book in book_list:
					if book.owner == user:
						book_list.remove(book)
						book_order.append(book)
						break
		for index, book in enumerate(book_order):
			BookOrder.objects.create(book=book, order=index)
