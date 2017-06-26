# coding: utf-8
from django.core.management.base import BaseCommand, CommandError

from ebookSystem.models import Book
from mysite.settings import *
import datetime
import os
import shutil

class Command(BaseCommand):
	help = 'review part status'
#	def add_arguments(self, parser):
#		parser.add_argument('reviewpart', nargs='*')

	def handle(self, *args, **options):
		book_folder = BASE_DIR +'/file/ebookSystem/document'
		folder_list = os.listdir(book_folder)
		book_ISBN_list = [ i.ISBN for i in Book.objects.all() ]
		for folder in folder_list:
			if folder not in book_ISBN_list:
				print(book_folder +'/' +folder)
				shutil.rmtree(book_folder +'/' +folder)

		for book in Book.objects.all():
			if not os.path.exists(book.path):
				book.delete()