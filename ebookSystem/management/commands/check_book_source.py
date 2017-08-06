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

		for book in Book.objects.all():
			try:
				for i in os.listdir(book.path):
					if i.split('.')[-1] == 'txt':
						book.source = 'txt'
						book.save()
					elif i.split('.')[-1] == 'epub':
						book.source = 'epub'
						book.save()
			except BaseException as e:
				print e