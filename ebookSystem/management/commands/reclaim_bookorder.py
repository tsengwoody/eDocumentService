# coding: utf-8
from django.core.management.base import BaseCommand, CommandError

from django.core.cache import cache
from ebookSystem.models import *

class Command(BaseCommand):
	help = 'review part status'
#	def add_arguments(self, parser):
#		parser.add_argument('reviewpart', nargs='*')

	def handle(self, *args, **options):
		BookOrder.refresh()