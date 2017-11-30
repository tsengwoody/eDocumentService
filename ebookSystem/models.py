# coding: utf-8
from django.db import models
from django.db.models import F,Q
from django.utils import timezone
from mysite.settings import BASE_DIR
from genericUser.models import User, ServiceInfo, Event
import glob,os
import datetime
import codecs
import shutil
from PIL import Image, ImageFont, ImageDraw
from bs4 import BeautifulSoup, NavigableString

def generic_serialized(self):
	serialize = {}
	for field in self._meta.fields:
		value = getattr(self, field.name)
		if isinstance(value, models.Model):
			id_ = field.name +'_id'
			field_id_value = getattr(self, id_)
			value = '{0}/{1}'.format(value.__class__.__name__, field_id_value)
		else:
			try:
				json.dumps(value)
			except:
				value = unicode(value)
		serialize.update({field.name: value})
	return serialize

class BookInfo(models.Model):
	ISBN = models.CharField(max_length=20, primary_key=True)
	bookname = models.CharField(max_length=255)
	author = models.CharField(max_length=255)
	house = models.CharField(max_length=255)
	date = models.DateField()
	bookbinding = models.CharField(max_length=255, blank=True, null=True)
	chinese_book_category = models.IntegerField(blank=True, null=True)
	order = models.CharField(max_length=255, blank=True, null=True)
	source = models.CharField(max_length=255, blank=True, null=True)

	def __unicode__(self):
		return self.bookname

	serialized = generic_serialized

class Book(models.Model):
	ISBN = models.CharField(max_length=20, primary_key=True)
	book_info = models.OneToOneField(BookInfo, related_name='book')
	path = models.CharField(max_length=255, blank=True, null=True)
	page_count = models.IntegerField(default = -1)
	part_count = models.IntegerField(default = 1)
	page_per_part = models.IntegerField(default=-1)
	finish_date = models.DateField(blank=True, null=True)
	priority = models.IntegerField(default=9)
	scaner = models.ForeignKey(User,blank=True, null=True, on_delete=models.SET_NULL, related_name='scan_book_set')
	owner = models.ForeignKey(User,blank=True, null=True, on_delete=models.SET_NULL, related_name='own_book_set')
	upload_date = models.DateField(default = timezone.now)
	is_private = models.BooleanField(default=False)
	SOURCE = (
		(u'self', u'self'),
		(u'txt', u'txt'),
		(u'epub', u'epub'),
	)
	source = models.CharField(max_length=20, choices=SOURCE)
	status = models.IntegerField(default=0)
	STATUS = {'inactive':0, 'active':1, 'edit':2, 'review':3, 'finish':4, 'sc_edit':5, 'sc_finish':6, 'an_edit':7, 'an_finish':8, 'final': 9, }

	def serialized(self):
		old_serialize = generic_serialized(self)
		serialize = {}
		for key in ['finish_date', 'upload_date', ]:
			serialize.update({
			key: old_serialize[key],
		})
		return serialize


	def __unicode__(self):
		return self.book_info.bookname

	def delete(self, *args, **kwargs):
		try:
			shutil.rmtree(self.path)
			Event.objects.filter(content_type__model='book', object_id=self.ISBN, ).delete()
		except:
			pass
		super(Book, self).delete(*args, **kwargs)

	def status_int2str(self):
		for k, v in self.STATUS.iteritems():
			if v == self.status:
				return k
		return 'unknown'

	def check_status(self):
		status = min([ part.status for part in self.ebook_set.all() ])
		self.status = status
		if self.status_int2str() == 'finish':
			self.finish_date = max([ i.deadline for i in self.ebook_set.all() ])
		elif self.status_int2str() == 'final':
			pass
		self.save()
		return status

	def create_EBook(self, page_list=[]):
		if page_list == []:
			if not len(self.ebook_set.all()) == 0:
				raise ValueError('part not 0')
			part_count = (self.page_count-1)/self.page_per_part+1
			for i in range(part_count):
				begin_page = i*self.page_per_part
				end_page = (i+1)*self.page_per_part-1
				if end_page >= self.page_count:
					end_page = self.page_count-1
				ISBN_part = '{0}-{1}'.format(self.ISBN, i+1)
				EBook.objects.create(book=self, part=i+1, ISBN_part=ISBN_part, begin_page=begin_page, end_page=end_page)
			self.part_count = len(self.ebook_set.all())
			self.save()
			return True
		elif page_list != []:
			if not len(self.ebook_set.all()) == 0:
				return False
			for page_info in page_list:
				part = page_info[0]
				begin_page = page_info[1]
				end_page = page_info[2]
				ISBN_part = '{0}-{1}'.format(self.ISBN, part)
				EBook.objects.create(book=self, part=part, ISBN_part=ISBN_part, begin_page=begin_page, end_page=end_page)
			self.part_count = len(self.ebook_set.all())
			self.save()
			return True

	def get_org_image(self, user):
		org_path = BASE_DIR +u'/static/ebookSystem/document/{0}/source/{1}'.format(self.book_info.ISBN, "org")
		source_path = self.path +u'/source'
		fileList=os.listdir(source_path)
		fileList = sorted(fileList)
		scan_page_list = [scan_page for scan_page in fileList if scan_page.split('.')[-1].lower() == 'jpg']
		scan_page_lists = []
		for i in range(self.part_count-1):
			scan_page_lists.append(
				scan_page_list[i*self.page_per_part:(i+1)*self.page_per_part]
			)
		scan_page_lists.append(
				scan_page_list[(self.part_count-1)*self.page_per_part:]
		)
		if not os.path.exists(org_path +'/' +scan_page_list[0]):
			self.create_org_image()
		default_page_url_list = [ u'{0}/{1}'.format(org_path, scan_page_list[i*self.page_per_part]).replace(BASE_DIR +'/static/', '') for i in range(self.part_count)]
		return [scan_page_lists, default_page_url_list]

	def create_org_image(self):
		org_path = BASE_DIR +u'/static/ebookSystem/document/{0}/source/{1}'.format(self.book_info.ISBN, "org")
		source_path = self.path +u'/source'
		fileList=os.listdir(source_path)
		fileList = sorted(fileList)
		scanPageList=[scanPage for scanPage in fileList if scanPage.split('.')[-1].lower() == 'jpg']
		if os.path.exists(org_path +'/' +scanPageList[0]):
			return False
		if not os.path.exists(org_path):
			os.makedirs(org_path, 0770)
		for s in scanPageList:
			shutil.copyfile(source_path +'/' +s, org_path +'/' +s)
		return True

	def set_page_count(self):
		source = self.path + u'/source'
		sourceFileList=os.listdir(source)
		page_count = 0
		for scanPage in sourceFileList:
			if scanPage.split('.')[-1].lower() == 'jpg':
				page_count = page_count + 1
		self.page_count = page_count
		self.save()
		return self.page_count

	def validate_folder(self):
		from utils import validate
		try:
			validate.validate_folder(
				os.path.join(self.path, 'OCR'),
				os.path.join(self.path, 'source'),
				self.page_per_part,
			)
		except BaseException as e:
			raise e

	def custom_epub_create(self, custom_epub, user):
		self.check_status()
		#準備epub文件
		from ebooklib import epub
		from utils.epub import txt2epub, html2epub, add_bookinfo
		info = {
			'ISBN': self.book_info.ISBN,
			'bookname': self.book_info.bookname,
			'author': self.book_info.author,
			'date': str(self.book_info.date),
			'house': self.book_info.house,
			'language': 'zh',
		}
		if self.status == self.STATUS['final']:
			final_epub = self.path +'/OCR/{0}.epub'.format(self.ISBN)
			try:
				book = epub.read_epub(final_epub)
				book = add_bookinfo(
					book,
					**info
				)
				book.set_identifier(user.username)
				epub.write_epub(custom_epub, book, {})
			except BaseException as e:
				raise SystemError('epub create fail:' +unicode(e))
		else:
			final_epub = self.path +'/temp/{0}.temp'.format(self.ISBN)
			final_dir = os.path.dirname(final_epub)
			if not os.path.exists(final_dir):
				os.mkdir(final_dir)
			try:
				part_list = [ file.get_clean_file() for file in self.ebook_set.all() ]
				html2epub(part_list, final_epub, **info)
				book = epub.read_epub(final_epub)
				book.set_identifier(user.username)
				epub.write_epub(custom_epub, book, {})
			except BaseException as e:
				raise SystemError('epub create fail (not final):' +unicode(e))

		return custom_epub

	def zip(self, user, password):
		from django.contrib.auth import authenticate
		user = authenticate(username=user.username, password=password)
		if user is None:
			raise SystemError(u'密碼輸入不正確')

		custom_epub = self.path +'/temp/{0}_{1}.epub'.format(self.ISBN, user.username)
		if not os.path.exists(os.path.dirname(custom_epub)):
			os.mkdir(os.path.dirname(custom_epub))
		custom_epub = self.custom_epub_create(custom_epub, user)

		#加入壓縮檔內
		import pyminizip
		custom_zip = self.path +'/temp/{0}_{1}.zip'.format(self.ISBN, user.username)
		zip_list = [custom_epub]
		try:
			pyminizip.compress_multiple(zip_list, custom_zip, password, 5)
			return custom_zip
		except BaseException as e:
			try:
				os.remove(custom_zip)
			except BaseException as e:
				raise SystemError('zip create fail remove dirname' +unicode(e))
			raise SystemError('zip create fail:' +unicode(e))

	def collect_finish_page_count(self):
		finish_page_count = 0
		for part in self.ebook_set.all():
			finish_page_count = finish_page_count + part.edited_page + (part.status==part.STATUS['finish'])
		return finish_page_count

	def collect_finish_part_count(self):
		finish_part_count = 0
		for part in self.ebook_set.all():
			finish_part_count = finish_part_count + (part.status==part.STATUS['finish'])
		return finish_part_count

	def collect_get_count(self):
		get_count = 0
		for part in self.ebook_set.all():
			if part.status >= part.STATUS['edit']:get_count = get_count +1
		return get_count

	def collect_service_hours(self):
		service_hours = 0
		for part in self.ebook_set.all():
			service_hours = service_hours + part.service_hours
		return 		service_hours

class EBook(models.Model):
	ISBN_part = models.CharField(max_length=20, primary_key=True)
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	part = models.IntegerField()
	begin_page = models.IntegerField()
	end_page = models.IntegerField()
	edited_page = models.IntegerField(default=0)
	number_of_times = models.IntegerField(default=1)
	editor = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='edit_ebook_set')
	deadline = models.DateField(blank=True, null=True)
	get_date = models.DateField(blank=True, null=True)
	service_hours = models.IntegerField(default=0)
	status = models.IntegerField(default=0)
	STATUS = {'inactive':0, 'active':1, 'edit':2, 'review':3, 'finish':4, 'sc_edit':5, 'sc_finish':6, 'an_edit':7, 'an_finish':8, 'final':9}
	sc_editor = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='sc_edit_ebook_set')
	sc_deadline = models.DateField(blank=True, null=True)
	sc_get_date = models.DateField(blank=True, null=True)
	sc_service_hours = models.IntegerField(default=0)
	an_editor = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='an_edit_ebook_set')
	an_deadline = models.DateField(blank=True, null=True)
	an_get_date = models.DateField(blank=True, null=True)

	def get_source_list(self):
		source_path = self.book.path +u'/source'
		file_list = os.listdir(source_path)
		file_list = sorted(file_list)
		scan_file_list = [scan_file for scan_file in file_list if scan_file.split('.')[-1].lower() == 'jpg']
		scan_file_list = scan_file_list[self.begin_page:self.end_page+1]
		scan_file_dict = dict(enumerate(scan_file_list))
		return scan_file_dict

	def status_int2str(self):
		for k, v in self.STATUS.iteritems():
			if v == self.status:
				return k
		return 'unknown'

	def get_character_count(self, encoding='utf-8'):
		with codecs.open(self.get_file(), 'r', encoding=encoding) as dstFile:
			dst_content = dstFile.read()
		dstSoup = BeautifulSoup(dst_content, 'html5lib')
		dst_content_text = dstSoup.get_text().replace('\n', '').replace('\r', '').replace('   ', '').replace('  ', '').replace(u' ', '')
		return len(dst_content_text)

	def change_status(self, direction, status, **kwargs):
		if not self.status +direction == self.STATUS[status]:
			return False

		#正向status變化
		if direction == 1:
			if self.status +direction == self.STATUS['active']:
				self.add_tag()
				with codecs.open(self.get_path('-finish'), 'w', encoding='utf-8') as finishFile:
					finishFile.write(u'\ufeff')
				try:
					editRecord = EditRecord.objects.get(part=self, category='based', number_of_times=self.number_of_times)
				except:
					editRecord = EditRecord.objects.create(part=self, category='based', number_of_times=self.number_of_times)
				self.status = self.status +direction
			elif self.status +direction == self.STATUS['edit']:
				self.editor = kwargs['user']
				self.get_date = timezone.now()
				self.deadline = kwargs['deadline']
				self.status = self.status +direction
			elif self.status +direction == self.STATUS['review']:
				self.edited_page = self.end_page -self.begin_page
				self.status = self.status +direction
			elif self.status +direction == self.STATUS['finish']:
				self.add_template_tag(self.get_path('-finish'), self.get_path('-ge'))
				self.clean_tag(self.get_path('-ge'), self.get_path('-ge'))
				self.clean_tag(self.get_path('-ge'), self.get_path('-sc'))
				try:
					editRecord = EditRecord.objects.get(part=self, category='based', number_of_times=self.number_of_times)
					editRecord.record_info()
					editRecord.group_ServiceInfo()
				except:
					return False
				try:
					editRecord = EditRecord.objects.get(part=self, category='advanced', number_of_times=self.number_of_times)
				except:
					editRecord = EditRecord.objects.create(part=self, category='advanced', number_of_times=self.number_of_times)
				self.status = self.status +direction
			elif self.status +direction == self.STATUS['sc_edit']:
				self.sc_editor = kwargs['user']
				self.sc_get_date = timezone.now()
				self.sc_deadline = self.sc_get_date + datetime.timedelta(days=2)
				self.status = self.status +direction
			elif self.status +direction == self.STATUS['sc_finish']:
				shutil.copy2(self.get_path('-sc'), self.get_path('-an'))
				try:
					editRecord = EditRecord.objects.get(part=self, category='advanced', number_of_times=self.number_of_times)
					editRecord.record_info()
					editRecord.group_ServiceInfo()
				except:
					return False
				self.status = self.status +direction
			elif self.status +direction == self.STATUS['an_edit']:
				self.an_editor = kwargs['user']
				self.an_get_date = timezone.now()
				self.an_deadline = self.an_get_date + datetime.timedelta(days=1)
				self.status = self.status +direction
			elif self.status +direction == self.STATUS['an_finish']:
				self.status = self.status +direction
			elif self.status +direction == self.STATUS['final']:
				self.status = self.status +direction

		#反向status變化
		elif direction == -1:
			if self.status +direction == self.STATUS['active']:
				self.editor=None
				self.get_date = None
				self.deadline = None
				self.status = self.status +direction
			elif self.status +direction == self.STATUS['edit']:
				self.edit_page = 0
				self.load_full_content()
				self.status = self.status +direction
			elif self.status +direction == self.STATUS['finish']:
				self.sc_editor = None
				self.sc_get_date = None
				self.sc_deadline = None
				self.status = self.status +direction
			elif self.status +direction == self.STATUS['sc_finish']:
				self.an_editor = None
				self.an_get_date = None
				self.an_deadline = None
				self.status = self.status +direction
			else:
				return False

		if direction == 9:
			if self.status +direction == self.STATUS['final']:
				self.status = self.status +direction

		#儲存並確認book object status
		self.save()
		self.book.check_status()
		return self.status

	def get_image(self, user):
		water_path = BASE_DIR +u'/static/ebookSystem/document/{0}/source/{1}'.format(self.book.book_info.ISBN, user.username)
		source_path = self.book.path +u'/source'
		fileList=os.listdir(source_path)
		fileList = sorted(fileList)
		scanPageList=[scanPage for scanPage in fileList if scanPage.split('.')[-1].lower() == 'jpg']
		scanPageList = scanPageList[self.begin_page:self.end_page+1]
		if not os.path.exists(water_path +'/' +scanPageList[0]):
			self.create_watermark_image(user)
		default_page_url = water_path +u'/' +scanPageList[self.edited_page]
		default_page_url=default_page_url.replace(BASE_DIR +'/static/', '')
		return [scanPageList, default_page_url]

	def get_path(self, string=''):
		if string == 'public':
			return self.book.path.replace('/file', '/static')
		elif string in ['-clean', '-ge', '-sc', '-an', ]:
			return self.book.path +'/OCR/part{0}{1}.html'.format(self.part, string)
		elif string in ['', '-edit', '-finish', '-final', ]:
			return self.book.path +'/OCR/part{0}{1}.txt'.format(self.part, string)


	def __unicode__(self):
		return self.book.book_info.bookname+u'-part'+str(self.part)

	def get_content(self, action='', encoding='utf-8'):
		filePath = self.get_path(action)
		with codecs.open(filePath, 'r', encoding=encoding) as sourceFile:
			source_content = sourceFile.read()
#		file_head = source_content[0]
#		source_content = source_content[1:]
		return source_content

	def set_content(self, finish_content, edit_content, encoding='utf-8', fileHead = u'\ufeff'):
		finishFilePath = self.get_path('-finish')
		editFilePath = self.get_path('-edit')
		with codecs.open(finishFilePath, 'a', encoding=encoding) as fileWrite:
			fileWrite.write(finish_content)
		with codecs.open(editFilePath, 'w', encoding=encoding) as fileWrite:
			fileWrite.write(edit_content)
		return True

	def load_full_content(self):
		edit_content = self.get_content('-edit')
		finish_content = self.get_content('-finish')
		self.set_content('', finish_content +edit_content)
		with codecs.open(self.get_path('-finish'), 'w', encoding='utf-8') as finishFile:
			finishFile.write(u' ')
		return finish_content +edit_content

	def get_org_image(self, user):
		org_path = BASE_DIR +u'/static/ebookSystem/document/{0}/source/{1}'.format(self.book.book_info.ISBN, "org")
		source_path = self.book.path +u'/source'
		fileList=os.listdir(source_path)
		fileList = sorted(fileList)
		scanPageList=[scanPage for scanPage in fileList if scanPage.split('.')[-1].lower() == 'jpg']
		scanPageList = scanPageList[self.begin_page:self.end_page+1]
		if not os.path.exists(org_path +'/' +scanPageList[0]):
			self.create_org_image()
		default_page_url = org_path +u'/' +scanPageList[self.edited_page]
		default_page_url=default_page_url.replace(BASE_DIR +'/static/', '')
		return [scanPageList, default_page_url]

	def create_org_image(self):
		org_path = BASE_DIR +u'/static/ebookSystem/document/{0}/source/{1}'.format(self.book.book_info.ISBN, "org")
		source_path = self.book.path +u'/source'
		fileList=os.listdir(source_path)
		fileList = sorted(fileList)
		scanPageList=[scanPage for scanPage in fileList if scanPage.split('.')[-1].lower() == 'jpg']
		scanPageList = scanPageList[self.begin_page:self.end_page+1]
		if os.path.exists(org_path +'/' +scanPageList[0]):
			return False
		if not os.path.exists(org_path):
			os.makedirs(org_path, 0770)
		for s in scanPageList:
			shutil.copyfile(source_path +'/' +s, org_path +'/' +s)
		return True

	def get_image(self, user):
		water_path = BASE_DIR +u'/static/ebookSystem/document/{0}/source/{1}'.format(self.book.book_info.ISBN, user.username)
		source_path = self.book.path +u'/source'
		fileList=os.listdir(source_path)
		fileList = sorted(fileList)
		scanPageList=[scanPage for scanPage in fileList if scanPage.split('.')[-1].lower() == 'jpg']
		scanPageList = scanPageList[self.begin_page:self.end_page+1]
		if not os.path.exists(water_path +'/' +scanPageList[0]):
			self.create_watermark_image(user)
		default_page_url = water_path +u'/' +scanPageList[self.edited_page]
		default_page_url=default_page_url.replace(BASE_DIR +'/static/', '')
		return [scanPageList, default_page_url]

	def create_watermark_image(self, user):
		water_path = BASE_DIR +u'/static/ebookSystem/document/{0}/source/{1}/'.format(self.book.book_info.ISBN, user.username)
		source_path = self.book.path +u'/source'
		font_file = BASE_DIR+u'/static/ebookSystem/font/wt014.ttf'
		fileList=os.listdir(source_path)
		fileList = sorted(fileList)
		scanPageList=[scanPage for scanPage in fileList if scanPage.split('.')[-1].lower() == 'jpg']
		scanPageList = scanPageList[self.begin_page:self.end_page+1]
		if os.path.exists(water_path +'/' +scanPageList[0]):
			return False
		if not os.path.exists(water_path):
			os.makedirs(water_path, 0770)
		for s in scanPageList:
			image_file=source_path +'/' +s
			self.add_watermark(str(user.username), font_file, 52, image_file, water_path)
		return True

	def add_watermark(self,text, fontname, fontsize, imagefile, output_dir):
		img0 = Image.new("RGBA", (1,1))
		draw0 = ImageDraw.Draw(img0)
		font = ImageFont.truetype(fontname, fontsize)
		t_width, t_height = draw0.textsize(unicode(text, 'UTF-8'), font=font)
		img = Image.new("RGBA", (t_width, t_height), (255,0,0,0))
		draw = ImageDraw.Draw(img)
		draw.text((0,0),unicode(text, 'UTF-8'), font=font, fill=(0,255,255,128))
		img2 = Image.open(imagefile)
		i_width, i_height = img2.size
		px = (i_width - t_width) / 2
		py = (i_height - t_height) / 2
		img2.paste(img, (px, py), img)
		imagefile = imagefile.split('/')[-1]
		imagefile = imagefile
		img2.save(output_dir + imagefile)
		del draw0, draw
		del img0, img, img2

	def add_tag(self, encoding='utf-8'):
		from utils import tag
		source = self.get_path()
		destination = self.get_path('-edit')
		tag.add_tag(source, destination)

	def add_template_tag(self, src, dst, encoding='utf-8'):
		from utils import tag
		tag.add_template_tag(src, dst)

	def clean_tag(self, src, dst, template='book_template.html', encoding='utf-8'):
		from utils import tag
		title = self.book.book_info.bookname +'-part{0}'.format(self.part)
		tag.clean_tag(src, dst, title)

	def replace(self):
		from utils.replace import replace
		shutil.copy2(self.get_clean_file(), self.get_path('-re'))
		replace(self.get_path('-re'))
		return self.get_path('-re')

	def get_file(self):
		if self.STATUS['finish'] <= self.status < self.STATUS['sc_finish']:
			return self.get_path('-ge')
		elif self.STATUS['sc_finish'] <= self.status < self.STATUS['an_finish']:
			return self.get_path('-sc')
		elif self.STATUS['an_finish'] <= self.status < self.STATUS['final']:
			return self.get_path('-an')
		elif self.STATUS['final'] <= self.status:
			return self.get_path('-final')
		else:
			return None

	def get_clean_file(self):
		try:
			shutil.copy2(self.get_file(), self.get_path('-clean'))
			return self.get_path('-clean')
		except:
			return None

	def zip(self, user, password):
		from django.contrib.auth import authenticate
		import pyminizip
		user = authenticate(username=user.username, password=password)
		if user is None:
			return False
		custom_zip = self.book.path +'/temp/{0}_{1}.zip'.format(self.ISBN_part, user.username)
		if not os.path.exists(os.path.dirname(custom_zip)):
			os.mkdir(os.path.dirname(custom_zip))
		zip_list = [self.get_clean_file()]
		try:
			pyminizip.compress_multiple(zip_list, custom_zip, password, 5)
			return custom_zip
		except BaseException as e:
			try:
				os.remove(custom_zip)
			except BaseException as e:
				pass
			return False

	def zip_full(self, ):
		from django.contrib.auth import authenticate
		import pyminizip
		zip_file_name = BASE_DIR +'/file/ebookSystem/document/{0}/OCR/{1}.zip'.format(self.book.book_info.ISBN, self.ISBN_part, )
		zip_list = [self.get_path(), self.get_path('-edit'), self.get_path('-finish'), ]
		try:
			pyminizip.compress_multiple(zip_list, zip_file_name, '', 5)
			return zip_file_name
		except BaseException as e:
			try:
				os.remove(zip_file_name)
				raise e
			except:
				raise e

	def edit_distance(self, src, dst, encoding='utf-8'):
		import Levenshtein
		with codecs.open(src, 'r', encoding=encoding) as srcFile:
			src_content = srcFile.read()
		srcSoup = BeautifulSoup(src_content, 'html5lib')
		src_content_text = srcSoup.get_text().replace('\n', '').replace('\r', '').replace('   ', '').replace('  ', '').replace(u' ', '')
		with codecs.open(dst, 'r', encoding=encoding) as dstFile:
			dst_content = dstFile.read()
		dstSoup = BeautifulSoup(dst_content, 'html5lib')
		dst_content_text = dstSoup.get_text().replace('\n', '').replace('\r', '').replace('   ', '').replace('  ', '').replace(u' ', '')
#	with codecs.open('temp.html', 'w', encoding='utf-8') as tempFile:
#		tempFile.write(dst_content_text)
		return Levenshtein.distance(src_content_text, dst_content_text)

	@staticmethod
	def split_content(content):
		content = content.split('<p>|----------|</p>\r\n')
		finish_content = content[0]
		edit_content = content[1]
		return [finish_content, edit_content]

class BookOrder(models.Model):
	book = models.OneToOneField(Book, related_name='bookorder')
	order = models.IntegerField()

	def __unicode__(self):
		return self.book.book_info.bookname

	@classmethod
	def refresh(cls):
		BookOrder.objects.all().delete()
		book_list = [ book for book in Book.objects.filter(Q(status=Book.STATUS['active'])|Q(status=Book.STATUS['edit'])).order_by('priority', 'upload_date') ]

		user_order = []
		for book in book_list:
			if book.owner not in user_order:
				user_order.append(book.owner)

		book_order = []
		while book_list:
			for user in user_order:
				for book in book_list:
					if book.owner == user:
						book_list.remove(book)
						book_order.append(book)
						break
		for index, book in enumerate(book_order):
			BookOrder.objects.create(book=book, order=index)

class GetBookRecord(models.Model):
	user = models.ForeignKey(User, related_name='getbookrecord_set')
	book = models.ForeignKey(Book, related_name='getbookrecord_set')
	get_time = models.DateTimeField(default = timezone.now)
	get_ip = models.GenericIPAddressField()

	def __unicode__(self):
		return u'{0}-{1}'.format(self.book, self.user)

class LibraryRecord(models.Model):
	user = models.ForeignKey(User, related_name='libraryrecord_set')
	book = models.ForeignKey(Book, related_name='libraryrecord_set')
	check_out_time = models.DateTimeField(blank=True, null=True)
	check_in_time = models.DateTimeField(blank=True, null=True)
	status = models.BooleanField(default=False)

	def __unicode__(self):
		return u'{0}-{1}'.format(self.book, self.user)

	def __init__(self, *args, **kwargs):
		super(LibraryRecord, self).__init__(*args, **kwargs)
		self.epub = BASE_DIR +'/file/ebookSystem/library/{0}.epub'.format(self.id)

	def check_out(self):
		if not os.path.exists(os.path.dirname(self.epub)):
			os.mkdir(os.path.dirname(self.epub))
		path = self.book.custom_epub_create(self.epub, self.user)

		self.check_out_time = timezone.now()
		self.check_in_time = self.check_out_time +datetime.timedelta(days=30)
		self.status = True
		self.save()

		return path

	def check_in(self):
		self.check_in_time = timezone.now()
		self.status = False
		self.save()
		try:
			os.remove(self.epub)
		except BaseException as e:
			pass
		return self.epub

class EditRecord(models.Model):
	part = models.ForeignKey(EBook, blank=True, null=True, on_delete=models.SET_NULL, related_name='editrecord_set')
	CATEGORY = (
		('based' , u'初階'),
		(u'advanced' , u'進階'),
	)
	category = models.CharField(max_length=10, choices=CATEGORY)
	number_of_times = models.IntegerField()
	editor = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='editrecord_set')
	get_date = models.DateField(blank=True, null=True)
	service_hours = models.IntegerField(default=0)
	stay_hours = models.IntegerField(default=0)
	serviceInfo = models.ForeignKey(ServiceInfo,blank=True, null=True, on_delete=models.SET_NULL, related_name='editrecord_set')

	class Meta:
		unique_together = (('part', 'category', 'number_of_times'),)

	def __unicode__(self):
		return self.part.ISBN_part

	def record_info(self):
		if self.category == 'based':
			self.editor = self.part.editor
			self.get_date = self.part.get_date
			self.stay_hours = self.part.service_hours
			self.save()
			self.service_hours = self.compute_service_hours()
		elif self.category == 'advanced':
			self.editor = self.part.sc_editor
			self.get_date = self.part.sc_get_date
			self.stay_hours = self.part.service_hours
			self.save()
			self.service_hours = self.part.sc_service_hours
		self.save()

	def group_ServiceInfo(self):
		month_ServiceInfo = None
		if self.get_date and self.editor:
			month = datetime.date(year=self.get_date.year, month=self.get_date.month, day=1)
			try:
				month_ServiceInfo = ServiceInfo.objects.get(user=self.editor, date=month)
			except:
				month_ServiceInfo = ServiceInfo.objects.create(user=self.editor, date=month)
			self.serviceInfo = month_ServiceInfo
			self.save()
		return month_ServiceInfo

	def compute_service_hours(self):
		service_hours = 0
		for editLog in self.editlog_set.filter(user=self.editor).order_by('order'):
			if editLog.edit_count != 0:
				service_hours = service_hours +1
				continue
			try:
				previous_editLog = self.editlog_set.all().get(order=editLog.order-1)
				if previous_editLog.edit_count != 0:
					service_hours = service_hours +1
			except:
				continue
		return service_hours

class EditLog(models.Model):
	edit_record = models.ForeignKey(EditRecord, blank=True, null=True, on_delete=models.SET_NULL, related_name='editlog_set')
	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='editlog_set')
	time = models.DateTimeField(default = timezone.now)
	order = models.IntegerField()
	edit_count = models.IntegerField()
#	page = models.IntegerField()

	def __unicode__(self):
		return self.edit_record.part.ISBN_part +'-{0}'.format(self.order)

'''	class Meta:
		indexes = [
			models.Index(fields=['book'], name='book_idx'),
			models.Index(fields=['part'], name='part_idx'),
		]'''

def add_watermark(self,text, fontname, fontsize, imagefile, output_dir):
	img0 = Image.new("RGBA", (1,1))
	draw0 = ImageDraw.Draw(img0)
	font = ImageFont.truetype(fontname, fontsize)
	t_width, t_height = draw0.textsize(unicode(text, 'UTF-8'), font=font)
	img = Image.new("RGBA", (t_width, t_height), (255,0,0,0))
	draw = ImageDraw.Draw(img)
	draw.text((0,0),unicode(text, 'UTF-8'), font=font, fill=(0,255,255,128))
	img2 = Image.open(imagefile)
	i_width, i_height = img2.size
	px = (i_width - t_width) / 2
	py = (i_height - t_height) / 2
	img2.paste(img, (px, py), img)
	imagefile = imagefile.split('/')[-1]
	imagefile = imagefile
	print output_dir+" "+imagefile + " saved..."
	img2.save(output_dir + imagefile)
	del draw0, draw
	del img0, img, img2
