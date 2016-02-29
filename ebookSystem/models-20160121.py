from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
class Editor(AbstractUser):
	last_contact = models.DateField(blank=True, null=True)
	def __unicode__(self):
		return self.username

class Book(models.Model):
	bookname = models.CharField(max_length=50)
	author = models.CharField(max_length=50)
	translator = models.CharField(max_length=50, blank=True, null=True)
	house = models.CharField(max_length=30)
	date = models.DateField()
	ISBN = models.CharField(max_length=20, blank=True, null=True)
	remark = models.CharField(max_length=255, blank=True, null=True)
	def __unicode__(self):
		return self.bookname

class EBook(models.Model):
	book = models.OneToOneField(Book)
	editor = models.ForeignKey(Editor,blank=True, null=True, on_delete=models.SET_NULL)
	is_finish = models.BooleanField(default=False)
	path = models.CharField(max_length=255, blank=True, null=True)
	scan_date = models.DateField(blank=True, null=True)
	edit_date = models.DateField(blank=True, null=True)
	remark = models.CharField(max_length=255, blank=True, null=True)
	def __unicode__(self):
		return self.book.bookname