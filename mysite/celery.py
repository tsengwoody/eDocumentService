from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
import django
django.setup()

from ebookSystem.models import Book

app = Celery('mysite')

# Using a string here means the worker will not have to
# mysite the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
	# Calls test('hello') every 10 seconds.
	sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

	# Calls test('world') every 30 seconds
	sender.add_periodic_task(30.0, test.s('world'), expires=10)

	# Executes every Monday morning at 7:30 a.m.
	sender.add_periodic_task(
		crontab(hour=7, minute=30, day_of_week=1),
		test.s('Happy Mondays!'),
	)

@app.task
def test(arg):
	print(arg)
