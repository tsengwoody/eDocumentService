# coding: utf-8
from django.core.management.base import BaseCommand, CommandError

from ebookSystem.models import *
import datetime

class Command(BaseCommand):
	help = 'review part status'
#	def add_arguments(self, parser):
#		parser.add_argument('reviewpart', nargs='*')

	def handle(self, *args, **options):
		eds = EditRecord.objects.filter(category='based').exclude(part=None)
		i = 0
		for ed in eds:
			try:
				path = ed.part.get_path('-edit')
				with io.open(path, 'r', encoding='utf-8') as f:
					ed.edit = f.read()
				path = ed.part.get_path('-finish')
				with io.open(path, 'r', encoding='utf-8') as f:
					ed.finish = f.read()
				ed.save()
				i = i+1
			except BaseException as e:
				print unicode(e) +'->' +ed.part.ISBN_part
		print i