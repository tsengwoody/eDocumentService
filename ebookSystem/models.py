# coding: utf-8
from django.db import models
from django.db.models.signals import *
from django.utils import timezone

from mysite.settings import PREFIX_PATH,INACTIVE, ACTIVE, EDIT, REVIEW, REVISE, FINISH
from genericUser.models import User
from guest.models import Guest
from account.models import Editor
import os
import datetime
import codecs

class Book(models.Model):
	ISBN = models.CharField(max_length=20, primary_key=True)
	bookname = models.CharField(max_length=50)
	author = models.CharField(max_length=50)
	house = models.CharField(max_length=30)
	date = models.DateField()
	path = models.CharField(max_length=255, blank=True, null=True)
	page_count = models.IntegerField(blank=True, null=True)
	part_count = models.IntegerField(blank=True, null=True)
	page_per_part = models.IntegerField(default=50)
	priority = models.IntegerField(default=0)
	scaner = models.ForeignKey(User,blank=True, null=True, on_delete=models.SET_NULL, related_name='scan_book_set')
	guests = models.ManyToManyField(Guest, related_name='own_book_set')
	status = models.IntegerField(default=INACTIVE)
	upload_date = models.DateField(default = timezone.now)
	remark = models.CharField(max_length=255, blank=True, null=True)
	def __unicode__(self):
		return self.bookname

	def create_EBook(self):
		if not (len(self.ebook_set.all()) == 0 and self.validate_folder()):
			return False
		for i in range(self.part_count):
			begin_page = i*self.page_per_part
			end_page = (i+1)*self.page_per_part-1
			if end_page >= self.page_count:
				end_page = self.page_count-1
			ISBN_part = self.ISBN + '-{0}'.format(i+1)
			part = EBook.objects.create(book=self, part=i+1, ISBN_part=ISBN_part, begin_page=begin_page, end_page=end_page)
		for i in range(1, self.part_count+1):
			edit_content = ''
			source = self.path +'/OCR/part{}.txt'.format(i)
			destination = self.path +'/OCR/part{}-edit.txt'.format(i)
			with codecs.open(source, 'r', encoding='utf-8') as sourceFile:
				for edit in sourceFile:
					if edit[-2:] == '\r\n':
						edit = '<p>' +edit[:-2] +'</p>' +edit[-2:]
					else:
						edit = '<p>' +edit +'</p>'
					edit_content = edit_content +edit
			edit_content = edit_content[0:3] +edit_content[4:]
			if edit_content[-2:] != '\r\n': edit_content=edit_content +'\r\n'
			with codecs.open(destination, 'w', encoding='utf-8') as destinationFile:
				destinationFile.write(u'\ufeff' +edit_content)
		for i in range(1, self.part_count+1):
			with codecs.open(self.path +'/OCR/part{}-finish.txt'.format(i), 'w', encoding='utf-8') as finishFile:
				finishFile.write(u'\ufeff')
		return True

	def validate_folder(self):
		source = self.path + u'/source'
		OCR = self.path + u'/OCR'
		partList = []
		OCRFileList = []
		sourceFileList = []
		try:
			OCRFileList = os.listdir(OCR)
			for file in OCRFileList:
				with codecs.open(os.path.join(OCR, file), 'r', encoding='utf-8') as fileRead:
					content=fileRead.read()
			sourceFileList=os.listdir(source)
		except:
			self.page_count = None
			self.part_count = None
			return False
		page_count = 0
		for scanPage in sourceFileList:
			if scanPage.split('.')[-1].lower() == 'jpg':
				page_count = page_count + 1
		part_count = (page_count-1)/self.page_per_part+1
		for i in range(part_count):
			partList.append('part{}.{}'.format(i+1, 'txt'))
		partSet = set(partList)
		for i in range(i):
			OCRFileList[i] = OCRFileList[i].lower()
		OCRFileSet = set(OCRFileList)
		self.page_count = page_count
		self.part_count = part_count
		return partSet.issubset(OCRFileSet)

	def collect_is_finish(self):
		is_finish = True
		for part in self.ebook_set.all():
			is_finish = is_finish and part.status == FINISH
		return is_finish

	def collect_finish_page_count(self):
		finish_page_count = 0
		for part in self.ebook_set.all():
			finish_page_count = finish_page_count + part.edited_page + (part.status==FINISH)
		return finish_page_count

	def collect_finish_part_count(self):
		finish_part_count = 0
		for part in self.ebook_set.all():
			finish_part_count = finish_part_count + (part.status==FINISH)
		return finish_part_count

	def collect_get_count(self):
		get_count = 0
		for part in self.ebook_set.all():
			if part.status >= EDIT:get_count = get_count +1
		return get_count

	def collect_service_hours(self):
		service_hours = 0
		for part in self.ebook_set.all():
			service_hours = service_hours + part.service_hours
		return 		service_hours

class EBook(models.Model):
	book = models.ForeignKey(Book)
	part = models.IntegerField()
	ISBN_part = models.CharField(max_length=23, primary_key=True)
	begin_page = models.IntegerField()
	end_page = models.IntegerField()
	edited_page = models.IntegerField(default=0)
	editor = models.ForeignKey(Editor,blank=True, null=True, on_delete=models.SET_NULL)
	status = models.IntegerField(default=ACTIVE)
	is_exchange = models.BooleanField(default=False)
	finish_date = models.DateField(blank=True, null=True)
	deadline = models.DateField(blank=True, null=True)
	get_date = models.DateField(blank=True, null=True)
	service_hours = models.IntegerField(default=0)
	remark = models.CharField(max_length=255, blank=True, null=True)



	def fuzzy_string_search(self, string, length=5, action=''):
		class SliceString():
			def __init__(self, start, end, source_content, source_index, destination_content, destination_index):
				self.start = start
				self.end = end
				self.source_index = source_index
				self.destination_index = destination_index
				self.source_content = source_content
				self.destination_content = destination_content
			
			def content_diff(self):
				temps = []
				for start, end in self.source_index:
					temps.append(self.source_content[start:end])
				for i, s in enumerate(temps):
					if s == '':
						temps[i] = u'□'
				tempd = []
				for start, end in self.destination_index:
					tempd.append(self.destination_content[start:end])
				for i, s in enumerate(tempd):
					if s == '':
						tempd[i] = u'□'
				content_list = zip(temps, tempd)
				return content_list

		import re
		import difflib
		[content, fileHead] = self.get_content(action)
		headString = string[0:length]
		tailString = string[-length:]
		destination_content = string
		ssl = []
		for headSearch in re.finditer(headString, content):
			for tailSearch in re.finditer(tailString, content):
				[headPosition, tailPosition] = [headSearch.start(), tailSearch.end()]
				if headPosition <= tailPosition:
					source_content = content[headPosition:tailPosition]
					matchList = difflib.SequenceMatcher(None, source_content, destination_content).get_matching_blocks()
					source_index = []
					destination_index = []
					for match in matchList:
						if match.size >2:
							source_index.append(match.a)
							source_index.append(match.a+match.size)
							destination_index.append(match.b)
							destination_index.append(match.b+match.size)
					temp = []
					for i in range(1, len(source_index)):
						temp.append([source_index[i-1], source_index[i]])
					source_index = temp
					temp = []
					for i in range(1, len(destination_index)):
						temp.append([destination_index[i-1], destination_index[i]])
					destination_index = temp
					ss = SliceString(start=headPosition, end=tailPosition, source_content=source_content, source_index=source_index, destination_content=destination_content, destination_index=destination_index)
					ssl.append(ss)
		return ssl

	def __unicode__(self):
		return self.book.bookname+u'-part'+str(self.part)

	def get_content(self, action='', encoding='utf-8'):
		filePath = self.book.path+u'/OCR/part{0}{1}.txt'.format(self.part, action)
		with codecs.open(filePath, 'r', encoding=encoding) as fileRead:
			firstLine=fileRead.next()
			fileHead=firstLine[0]
			content = firstLine[1:]
			for i in fileRead:
				content = content+i
		return [content,fileHead]

	def set_content(self, finish_content, edit_content, encoding='utf-8', fileHead = u'\ufeff'):
		finishFilePath = self.book.path+u'/OCR/part{0}-finish.txt'.format(self.part)
		editFilePath = self.book.path+u'/OCR/part{0}-edit.txt'.format(self.part)
		with codecs.open(finishFilePath, 'a', encoding=encoding) as fileWrite:
			fileWrite.write(finish_content)
		with codecs.open(editFilePath, 'w', encoding=encoding) as fileWrite:
			fileWrite.write(fileHead+edit_content)
		return True

	def get_image(self):
		sourcePath = self.book.path +u'/source'
		fileList=os.listdir(sourcePath)
		fileList = sorted(fileList)
		scanPageList=[scanPage for scanPage in fileList if scanPage.split('.')[-1].lower() == 'jpg']
		scanPageList = scanPageList[self.begin_page:self.end_page+1]
		defaultPage = scanPageList[self.edited_page]
		defaultPageURL = sourcePath +u'/' +defaultPage
		defaultPageURL=defaultPageURL.replace(PREFIX_PATH +'static/', '')
		return [scanPageList, defaultPage, defaultPageURL]

	def edit_distance(self, action, encoding='utf-8'):
		import Levenshtein
		if action == 'origin-finish':
			source = self.book.path+u'/OCR/part{0}.txt'.format(self.part)
			finish = self.book.path+u'/OCR/part{0}-finish.txt'.format(self.part)
			edit = self.book.path+u'/OCR/part{0}-edit.txt'.format(self.part)
			with codecs.open(finish, 'r', encoding=encoding) as finishFile:
				finishContent = finishFile.read()
			with codecs.open(edit, 'r', encoding=encoding) as editFile:
				editContent = editFile.read()
			destinationContent = finishContent+editContent[1:]
		if action == 'finish-final':
			source = self.book.path+u'/OCR/part{0}-finish.txt'.format(self.part)
			destination = self.book.path+u'/OCR/part{0}-final.txt'.format(self.part)
			with codecs.open(destination, 'r', encoding=encoding) as destinationFile:
				destinationContent = destinationFile.read()
		with codecs.open(source, 'r', encoding=encoding) as sourceFile:
			sourceContent = sourceFile.read()
		return Levenshtein.distance(sourceContent, destinationContent)

	@staticmethod
	def split_content(content):
		content = content.split('<p>|----------|</p>\r\n')
		finish_content = content[0]
		edit_content = content[1]
		return [finish_content, edit_content]

class ReviseContentAction(models.Model):
	ebook = models.ForeignKey('EBook')
	content = models.CharField(max_length=1000)

def pre_save_Book(**kwargs):
	book = kwargs.get('instance')
	if book.page_count == None or book.part_count == None or book.path == None:
		book.path = PREFIX_PATH + u'static/ebookSystem/document/{0}'.format(book.ISBN)
		result = book.validate_folder()

pre_save.connect(pre_save_Book, Book)
