# coding: utf-8
from django.db import models
from django.db.models.signals import *
from django.utils import timezone

from mysite import settings
from genericUser.models import User
from guest.models import Guest
from account.models import Editor
import os
import datetime

class Book(models.Model):
	bookname = models.CharField(max_length=50)
	author = models.CharField(max_length=50)
	translator = models.CharField(max_length=50, blank=True, null=True)
	house = models.CharField(max_length=30)
	date = models.DateField()
	ISBN = models.CharField(max_length=20)
	path = models.CharField(max_length=255, blank=True, null=True)
	page_count = models.IntegerField(blank=True, null=True)
	part_count = models.IntegerField(blank=True, null=True)
	page_per_part = models.IntegerField(default=50)
	guest = models.ForeignKey(Guest,blank=True, null=True, on_delete=models.SET_NULL)
	is_active = models.BooleanField(default=False)
	upload_date = models.DateField(default = timezone.now())
	remark = models.CharField(max_length=255, blank=True, null=True)
	def __unicode__(self):
		return self.bookname

	def vaildate_folder(self):
		source = self.path + u'/source'
		OCR = self.path + u'/OCR'
		try:
			fileList=os.listdir(source)
			fileList=os.listdir(OCR)
		except:
			return False
		partList = []
		fileList = []
		for i in range(self.part_count):
			partList.append('part{}'.format(i+1))
		partSet = set(partList)
		fileSet = set(fileList)
		return partSet.issubset(fileSet)

	def collect_is_finish(self):
		is_finish = True
		for part in self.ebook_set.all():
			is_finish = is_finish and part.is_finish
		return is_finish

	def collect_finish_page_count(self):
		finish_page_count = 0
		for part in self.ebook_set.all():
			finish_page_count = finish_page_count + part.edited_page + part.is_finish
		return finish_page_count

	def collect_finish_part_count(self):
		finish_part_count = 0
		for part in self.ebook_set.all():
			finish_part_count = finish_part_count + part.is_finish
		return finish_part_count

	def collect_get_count(self):
		get_count = 0
		for part in self.ebook_set.all():
			if part.editor:get_count = get_count +1
		return get_count

	def collect_service_hours(self):
		service_hours = 0
		for part in self.ebook_set.all():
			service_hours = service_hours + part.service_hours
		return 		service_hours

class EBook(models.Model):
	book = models.ForeignKey(Book)
	part = models.IntegerField()
	begin_page = models.IntegerField()
	end_page = models.IntegerField()
	edited_page = models.IntegerField(default=0)
	editor = models.ForeignKey(Editor,blank=True, null=True, on_delete=models.SET_NULL)
	is_finish = models.BooleanField(default=False)
	is_edited = models.BooleanField(default=False)
	is_exchange = models.BooleanField(default=False)
	edit_date = models.DateTimeField(blank=True, null=True)
	finish_date = models.DateField(blank=True, null=True)
	deadline = models.DateField(blank=True, null=True)
	get_date = models.DateField(blank=True, null=True)
	service_hours = models.IntegerField(default=0)
	remark = models.CharField(max_length=255, blank=True, null=True)

	class Meta:
		unique_together = ('book', 'part',)

	def __unicode__(self):
		return self.book.bookname+u'-part'+str(self.part)

def pre_save_Book(**kwargs):
	book = kwargs.get('instance')
	if book.page_count == None or book.part_count == None:
		book.path = settings.PREFIX_PATH + u'static/ebookSystem/document/{0}'.format(book.bookname)
		try:
			fileList=os.listdir(book.path+u'/source')
		except:
			print 'not folder'
			return -1
		book.page_count=0
		for scanPage in fileList:
			if scanPage.split('.')[-1]=='jpg':
				book.page_count = book.page_count+1
		print 'set page_count and part_count'
		book.part_count = book.page_count/book.page_per_part+1
		return 1
	return 0

def post_save_Book(**kwargs):
	book = kwargs.get('instance')
	if len(book.ebook_set.all()) == 0 and book.part_count and book.page_count:
		createEBookBatch(book)
	else:
		print 'The ebook is already exist'

pre_save.connect(pre_save_Book, Book)
post_save.connect(post_save_Book, Book)

def createEBookBatch(book):
	print u'create ebook batch {0}'.format(book.bookname)
	for i in range(book.part_count):
		begin_page = i*book.page_per_part
		end_page = (i+1)*book.page_per_part-1
		if end_page >= book.page_count:
			end_page = book.page_count-1
		part = EBook(book=book, part=i+1, begin_page=begin_page, end_page=end_page)
		part.save()
	return 1