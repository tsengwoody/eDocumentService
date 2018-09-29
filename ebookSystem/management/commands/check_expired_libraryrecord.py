# coding: utf-8
from django.core.management.base import BaseCommand, CommandError

from ebookSystem.models import LibraryRecord
import datetime

class Command(BaseCommand):
	help = 'review part status'
#	def add_arguments(self, parser):
#		parser.add_argument('reviewpart', nargs='*')

	def handle(self, *args, **options):
		for lr in LibraryRecord.objects.filter(status=True):
			if lr.check_in_time and lr.check_in_time.date() < datetime.date.today():
				lr.check_in()