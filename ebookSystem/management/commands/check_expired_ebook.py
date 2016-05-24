# coding: utf-8
from django.core.management.base import BaseCommand, CommandError

from account.models import *
from ebookSystem.models import *
from genericUser.models import *
from guest.models import *
import datetime

class Command(BaseCommand):
	help = 'review part status'
#	def add_arguments(self, parser):
#		parser.add_argument('reviewpart', nargs='*')

	def handle(self, *args, **options):
		for part in EBook.objects.all():
			if part.deadline and part.deadline < datetime.date.today():
				part.editor=None
				part.get_date = None
				part.deadline = None
				part.status = ACTIVE
				part.save()