# coding: utf-8
from django.core.management.base import BaseCommand, CommandError

from ebookSystem.models import EBook
import datetime

class Command(BaseCommand):
	help = 'review part status'
#	def add_arguments(self, parser):
#		parser.add_argument('reviewpart', nargs='*')

	def handle(self, *args, **options):
		for part in EBook.objects.all():
			if part.status == EBook.STATUS['edit'] and part.deadline and part.deadline < datetime.date.today():
				part.change_status(-1, 'active')