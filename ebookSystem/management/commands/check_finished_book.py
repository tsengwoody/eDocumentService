# coding: utf-8
from django.core.management.base import BaseCommand, CommandError

from account.models import *
from ebookSystem.models import *
from genericUser.models import *
from guest.models import *
import datetime

class Command(BaseCommand):
	help = 'review part status'

	def handle(self, *args, **options):
		for book in Book.objects.all():
			if book.collect_finish_part_count() == book.part_count:
				book.status = FINISH
				book.save()