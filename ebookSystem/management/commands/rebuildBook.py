from django.core.management.base import BaseCommand, CommandError
from ebookSystem.models import *

class Command(BaseCommand):
	help = 'check whether have new book'
	def add_arguments(self, parser):
		parser.add_argument('rebulid', nargs='*')

	def handle(self, *args, **options):
		self.stdout.write(self.args)