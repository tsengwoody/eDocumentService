# coding: utf-8
from django.core.management.base import BaseCommand, CommandError
from ebookSystem.models import *
from mysite.settings import BASE_DIR

import os
import shutil

class Command(BaseCommand):
	help = 'check DB and file system identical'
#	def add_arguments(self, parser):
#		parser.add_argument('reviewpart', nargs='*')

	def handle(self, *args, **options):
		base_path = BASE_DIR +'/file/ebookSystem/document/'
		book_folders = os.listdir(base_path)
		count = 0
		for ISBN in book_folders:
			if len(Book.objects.filter(ISBN=ISBN))==0:
				print(ISBN)
				path = base_path +'/' +ISBN
				print(os.listdir(path))
				shutil.rmtree(path)
				count = count +1
		print(count)
