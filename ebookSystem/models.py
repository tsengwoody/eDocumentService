import sys
from django.db import models
from django.db.models import F, Q
from django.utils import timezone
from mysite.settings import BASE_DIR
from genericUser.models import User, ServiceInfo, Organization
import glob, os
import datetime
import codecs
import io
import shutil
#from PIL import Image, ImageFont, ImageDraw
from bs4 import BeautifulSoup, NavigableString


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

	def __str__(self):
		return self.bookname

	@property
	def index_category(self):
		return self.book.index_category


class Book(models.Model):
	ISBN = models.CharField(max_length=20, primary_key=True)
	book_info = models.OneToOneField(BookInfo,
		on_delete=models.SET_NULL,
		blank=True,
		null=True,
		related_name='book')
	page_count = models.IntegerField(default=-1)
	part_count = models.IntegerField(default=1)
	page_per_part = models.IntegerField(default=-1)
	finish_date = models.DateField(blank=True, null=True)
	priority = models.IntegerField(default=9)
	scaner = models.ForeignKey(User,
		blank=True,
		null=True,
		on_delete=models.SET_NULL,
		related_name='scan_book_set')
	org = models.ForeignKey(Organization,
		on_delete=models.SET_NULL,
		blank=True,
		null=True,
		related_name='book_set')
	category = models.ForeignKey('Category',
		related_name='book_set',
		blank=True,
		null=True,
		on_delete=models.SET_NULL)
	index_category = models.ForeignKey('IndexCategory', related_name='book_set', blank=True, null=True, on_delete=models.SET_NULL)
	index_categorys = models.ManyToManyField('IndexCategory',
		blank=True,
		related_name="books")
	owner = models.ForeignKey(User,
		blank=True,
		null=True,
		on_delete=models.SET_NULL,
		related_name='own_book_set')
	upload_date = models.DateField(default=timezone.now)
	is_private = models.BooleanField(default=False)
	SOURCE = (
		(u'self', u'self'),
		(u'txt', u'txt'),
		(u'epub', u'epub'),
	)
	source = models.CharField(max_length=20, choices=SOURCE)
	status = models.IntegerField(default=0)
	STATUS = {
		'inactive': 0,
		'active': 1,
		'edit': 2,
		'review': 3,
		'finish': 4,
		'final': 5,
	}

	def __init__(self, *args, **kwargs):
		super(Book, self).__init__(*args, **kwargs)
		self.path = BASE_DIR + '/file/ebookSystem/document/{0}'.format(
			self.ISBN)

	def __str__(self):
		return self.book_info.bookname

	def delete(self, *args, **kwargs):
		try:
			shutil.rmtree(self.path)
		except:
			pass
		super(Book, self).delete(*args, **kwargs)

	def status_int2str(self):
		for k, v in self.STATUS.iteritems():
			if v == self.status:
				return k
		return 'unknown'

	def check_status(self):
		if self.status < 0:
			return -1

		status = min([part.status for part in self.ebook_set.all()])
		self.status = status

		if self.status == self.STATUS['finish']:
			self.finish_date = max([i.deadline for i in self.ebook_set.all()])
		elif self.status == self.STATUS['final']:
			pass
		self.save()
		return status

	def create_EBook(self, page_list=[]):
		if page_list == []:
			if not len(self.ebook_set.all()) == 0:
				raise ValueError('part not 0')
			part_count = int((self.page_count - 1) / self.page_per_part) + 1
			for i in range(part_count):
				begin_page = i * self.page_per_part
				end_page = (i + 1) * self.page_per_part - 1
				if end_page >= self.page_count:
					end_page = self.page_count - 1
				ISBN_part = '{0}-{1}'.format(self.ISBN, i + 1)
				EBook.objects.create(book=self,
					part=i + 1,
					ISBN_part=ISBN_part,
					begin_page=begin_page,
					end_page=end_page)
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
				EBook.objects.create(book=self,
					part=part,
					ISBN_part=ISBN_part,
					begin_page=begin_page,
					end_page=end_page)
			self.part_count = len(self.ebook_set.all())
			self.save()
			return True

	def set_page_count(self):
		source = self.path + u'/source'
		sourceFileList = os.listdir(source)
		page_count = 0
		for scanPage in sourceFileList:
			if scanPage.split('.')[-1].lower() == 'jpg':
				page_count = page_count + 1
		self.page_count = page_count
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

	def realtime_epub_create(self):
		final_epub = self.path + '/OCR/{0}.epub'.format(self.ISBN)
		try:
			part_list = [
				file.get_clean_file() for file in self.ebook_set.all()
			]
			from utils.epub import html2epub
			info = {
				'ISBN': self.book_info.ISBN,
				'bookname': self.book_info.bookname,
				'author': self.book_info.author,
				'date': str(self.book_info.date),
				'house': self.book_info.house,
				'language': 'zh',
			}
			html2epub(part_list, final_epub, **info)
		except BaseException as e:
			raise SystemError('epub create fail (not final):' + str(e))

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
		if self.status == 5 and self.source != 'self':
			final_epub = self.path + '/OCR/{0}.epub'.format(self.ISBN)
			try:
				book = epub.read_epub(final_epub)
				book = add_bookinfo(book, **info)
				book.set_identifier(user.username)
				epub.write_epub(custom_epub, book, {})
			except BaseException as e:
				raise SystemError('epub create fail:' + str(e))
		else:
			final_epub = self.path + '/temp/{0}.temp'.format(self.ISBN)
			final_dir = os.path.dirname(final_epub)
			if not os.path.exists(final_dir):
				os.mkdir(final_dir)
			try:
				part_list = [
					file.get_clean_file()
					for file in self.ebook_set.all().order_by('part')
				]
				html2epub(part_list, final_epub, **info)
				book = epub.read_epub(final_epub)
				book.set_identifier(user.username)
				epub.write_epub(custom_epub, book, {})
			except BaseException as e:
				raise SystemError('epub create fail (not final):' + str(e))

		return custom_epub

	def custom_txt_create(self, custom_txt, user):
		self.check_status()
		#準備epub文件
		from ebooklib import epub
		from utils.epub import html2txt, epub2txt
		info = {
			'ISBN': self.book_info.ISBN,
			'bookname': self.book_info.bookname,
			'author': self.book_info.author,
			'date': str(self.book_info.date),
			'house': self.book_info.house,
			'language': 'zh',
		}
		if self.status == 5 and self.source != 'self':
			final_txt = self.path + '/OCR/{0}.epub'.format(self.ISBN)
			try:
				epub2txt(final_txt, custom_txt)
			except BaseException as e:
				raise SystemError('epub create fail:' + str(e))
		else:
			final_txt = self.path + '/temp/{0}.temp'.format(self.ISBN)
			final_dir = os.path.dirname(final_txt)
			if not os.path.exists(final_dir):
				os.mkdir(final_dir)
			try:
				part_list = [
					file.get_clean_file() for file in self.ebook_set.all()
				]
				html2txt(part_list, custom_txt)
			except BaseException as e:
				raise SystemError('epub create fail (not final):' + str(e))

		with io.open(custom_txt, 'a', encoding='utf-8') as f:
			f.write(str(user.id))

		return custom_txt

	def zip(self, user, password, format):
		from django.contrib.auth import authenticate
		user = authenticate(username=user.username, password=password)
		if user is None:
			raise SystemError(u'密碼輸入不正確')

		custom_path = self.path + '/temp/{0}_{1}.{2}'.format(
			self.ISBN, user.username, format)
		if not os.path.exists(os.path.dirname(custom_path)):
			os.mkdir(os.path.dirname(custom_path))
		if format == 'epub':
			custom_path = self.custom_epub_create(custom_path, user)
		elif format == 'txt':
			custom_path = self.custom_txt_create(custom_path, user)

		return custom_path

		#加入壓縮檔內
		import pyminizip
		custom_zip = self.path + '/temp/{0}_{1}.zip'.format(
			self.ISBN, user.username)
		zip_list = [custom_path]
		try:
			pyminizip.compress_multiple(zip_list, [], custom_zip, password, 5)
			return custom_zip
		except BaseException as e:
			raise SystemError('zip create fail:' + str(e))
			try:
				os.remove(custom_zip)
			except BaseException as e:
				raise SystemError('zip create fail remove dirname' + str(e))
			raise SystemError('zip create fail:' + str(e))

	def collect_finish_page_count(self):
		finish_page_count = 0
		for part in self.ebook_set.all():
			finish_page_count = finish_page_count + part.edited_page + (
				part.status == part.STATUS['finish'])
		return finish_page_count

	def collect_finish_part_count(self):
		finish_part_count = 0
		for part in self.ebook_set.all():
			finish_part_count = finish_part_count + (part.status
				== part.STATUS['finish'])
		return finish_part_count

	def collect_get_count(self):
		get_count = 0
		for part in self.ebook_set.all():
			if part.status >= part.STATUS['edit']: get_count = get_count + 1
		return get_count

	def collect_service_hours(self):
		service_hours = 0
		for part in self.ebook_set.all():
			service_hours = service_hours + part.service_hours
		return service_hours


class EBook(models.Model):
	ISBN_part = models.CharField(max_length=20, primary_key=True)
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	part = models.IntegerField()
	begin_page = models.IntegerField()
	end_page = models.IntegerField()
	edited_page = models.IntegerField(default=0)
	number_of_times = models.IntegerField(default=1)
	editor = models.ForeignKey(User,
		blank=True,
		null=True,
		on_delete=models.SET_NULL,
		related_name='edit_ebook_set')
	deadline = models.DateField(blank=True, null=True)
	get_date = models.DateField(blank=True, null=True)
	service_hours = models.IntegerField(default=0)
	status = models.IntegerField(default=0)
	STATUS = {
		'inactive': 0,
		'active': 1,
		'edit': 2,
		'review': 3,
		'finish': 4,
		'final': 5,
	}

	def get_source_list(self):
		source_path = self.book.path + u'/source'
		try:
			file_list = os.listdir(source_path)
			file_list = sorted(file_list)
			scan_file_list = [
				scan_file for scan_file in file_list
				if scan_file.split('.')[-1].lower() == 'jpg'
			]
			scan_file_list = scan_file_list[self.begin_page:self.end_page + 1]
			scan_file_dict = dict(enumerate(scan_file_list))
			return scan_file_dict
		except:
			return {}

	def status_int2str(self):
		for k, v in self.STATUS.iteritems():
			if v == self.status:
				return k
		return 'unknown'

	def onactive(self):
		if not self.status == self.STATUS['finish']:
			raise SystemError('status not finish cant onactive')

		self.change_status(-4, 'inactive')
		self.change_status(1, 'active', category='based')

	def change_status(self, direction, status, **kwargs):
		if not self.status + direction == self.STATUS[status]:
			raise SystemError('direction and status not match')

		#正向status變化
		if direction == 1:
			if self.status + direction == self.STATUS['active']:

				try:
					editRecord = EditRecord.objects.get(part=self,
						number_of_times=self.number_of_times)
				except:
					editRecord = EditRecord.objects.create(part=self,
						number_of_times=self.number_of_times,
						category=kwargs['category'])

				# new use DB to storage text
				editRecord.textimport()

				self.status = self.status + direction
			elif self.status + direction == self.STATUS['edit']:
				self.editor = kwargs['user']
				self.get_date = datetime.date.today()
				self.deadline = kwargs['deadline']
				self.status = self.status + direction
			elif self.status + direction == self.STATUS['review']:
				self.edited_page = self.end_page - self.begin_page
				self.status = self.status + direction
			elif self.status + direction == self.STATUS['finish']:

				editRecord = EditRecord.objects.get(part=self,
					number_of_times=self.number_of_times)
				editRecord.record_info()
				editRecord.textexport()

				self.status = self.status + direction
			elif self.status + direction == self.STATUS['final']:
				self.status = self.status + direction
			else:
				return False

		#反向status變化
		elif direction == -1:
			if self.status + direction == self.STATUS['active']:
				self.editor = None
				self.get_date = None
				self.deadline = None
				self.status = self.status + direction
			elif self.status + direction == self.STATUS['edit']:
				self.edited_page = 0
				self.deadline = datetime.date.today() + datetime.timedelta(
					days=3)
				self.load_full_content()
				self.status = self.status + direction
			else:
				return False

		if direction == -4:  #再校對
			self.number_of_times += 1
			self.edited_page = 0
			self.editor = None
			self.get_date = None
			self.deadline = None
			self.service_hours = 0
			self.status = self.status + direction

		if direction == 5:
			if self.status + direction == self.STATUS['final']:
				self.status = self.status + direction

		#儲存並確認book object status
		self.save()
		self.book.check_status()
		return self.status

	def get_path(self, string=''):
		if string == 'public':
			return self.book.path.replace('/file', '/static')
		elif string in [
			'-clean',
			'-ge',
			'-sc',
			'-an',
		]:
			return self.book.path + '/OCR/part{0}{1}.html'.format(
				self.part, string)
		elif string in [
			'',
			'-edit',
			'-finish',
			'-final',
		]:
			return self.book.path + '/OCR/part{0}{1}.txt'.format(
				self.part, string)

	def __str__(self):
		return self.book.book_info.bookname + u'-part' + str(self.part)

	def current_editrecord(self):
		try:
			editRecord = EditRecord.objects.get(part=self,
				number_of_times=self.number_of_times)
		except:
			return None
		return editRecord

	def get_content(self):
		editRecord = EditRecord.objects.get(part=self,
			number_of_times=self.number_of_times)
		return (editRecord.finish, editRecord.edit)

	def set_content(self, finish_content, edit_content):
		editRecord = EditRecord.objects.get(part=self,
			number_of_times=self.number_of_times)
		editRecord.edit = edit_content
		editRecord.finish = finish_content
		editRecord.save()
		return (editRecord.finish, editRecord.edit)

	def load_full_content(self):
		editRecord = EditRecord.objects.get(part=self,
			number_of_times=self.number_of_times)
		editRecord.edit = editRecord.finish + editRecord.edit
		editRecord.finish = ''
		editRecord.save()
		return editRecord.edit

	def recover_content(self):
		editRecord = EditRecord.objects.get(part=self,
			number_of_times=self.number_of_times)
		editRecord.edit = editRecord.source_text()
		editRecord.finish = ''
		editRecord.save()

	def create_watermark_image(self, user):
		water_path = BASE_DIR + u'/static/ebookSystem/document/{0}/source/{1}/'.format(
			self.book.book_info.ISBN, user.username)
		source_path = self.book.path + u'/source'
		font_file = BASE_DIR + u'/static/ebookSystem/font/wt014.ttf'
		fileList = os.listdir(source_path)
		fileList = sorted(fileList)
		scanPageList = [
			scanPage for scanPage in fileList
			if scanPage.split('.')[-1].lower() == 'jpg'
		]
		scanPageList = scanPageList[self.begin_page:self.end_page + 1]
		if os.path.exists(water_path + '/' + scanPageList[0]):
			return False
		if not os.path.exists(water_path):
			os.makedirs(water_path, 755)
		for s in scanPageList:
			image_file = source_path + '/' + s
			self.add_watermark(str(user.username), font_file, 52, image_file,
				water_path)
		return True

	def add_watermark(self, text, fontname, fontsize, imagefile, output_dir):
		img0 = Image.new("RGBA", (1, 1))
		draw0 = ImageDraw.Draw(img0)
		font = ImageFont.truetype(fontname, fontsize)
		t_width, t_height = draw0.textsize(str(text, 'UTF-8'), font=font)
		img = Image.new("RGBA", (t_width, t_height), (255, 0, 0, 0))
		draw = ImageDraw.Draw(img)
		draw.text((0, 0),
			str(text, 'UTF-8'),
			font=font,
			fill=(0, 255, 255, 128))
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

	def get_clean_file(self):
		clean_file = self.get_path('-clean')
		with io.open(clean_file, 'w', encoding='utf-8') as f:
			f.write(self.current_editrecord().finish)
		return clean_file

	def zip(self, user, password):
		from django.contrib.auth import authenticate
		import pyminizip
		user = authenticate(username=user.username, password=password)
		if user is None:
			return False
		custom_zip = self.book.path + '/temp/{0}_{1}.zip'.format(
			self.ISBN_part, user.username)
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
		zip_file_name = BASE_DIR + '/file/ebookSystem/document/{0}/OCR/{1}.zip'.format(
			self.book.book_info.ISBN,
			self.ISBN_part,
		)
		zip_list = [
			self.get_path(),
			self.get_path('-edit'),
			self.get_path('-finish'),
		]
		try:
			pyminizip.compress_multiple(zip_list, zip_file_name, '', 5)
			return zip_file_name
		except BaseException as e:
			try:
				os.remove(zip_file_name)
				raise e
			except:
				raise e

	@staticmethod
	def split_content(content):
		content = content.split('<p>|----------|</p>')
		finish_content = content[0]
		edit_content = content[1]
		if not len(content) == 2:
			raise SystemError('save mark error')
		return [finish_content, edit_content]


class BookOrder(models.Model):
	book = models.OneToOneField(Book,
		on_delete=models.CASCADE,
		related_name='bookorder')
	order = models.IntegerField()

	def __str__(self):
		return self.book.book_info.bookname

	@classmethod
	def refresh(cls):
		BookOrder.objects.all().delete()

		# 針對每個單位各自產生領書的 queue
		for org in Organization.objects.all():

			# 書籍是未領取(active)或校對中(edit)且是該單位的書
			book_list = [
				book for book in Book.objects.filter((Q(
				status=Book.STATUS['active']) | Q(status=Book.STATUS['edit']))
				& Q(org=org)).order_by('priority', 'upload_date')
			]

			# 取得的書籍中以 user group by 並且有 user 排序
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
	user = models.ForeignKey(User,
		on_delete=models.SET_NULL,
		blank=True,
		null=True,
		related_name='getbookrecord_set')
	book = models.ForeignKey(Book,
		on_delete=models.CASCADE,
		related_name='getbookrecord_set')
	get_time = models.DateTimeField(default=timezone.now)
	get_ip = models.GenericIPAddressField()
	FORMAT = (
		('epub', 'epub'),
		('txt', 'txt'),
		('online', 'online'),
	)
	format = models.CharField(max_length=10, choices=FORMAT)

	def __str__(self):
		return u'{0}-{1}'.format(self.book, self.user)


class Library(models.Model):
	check_out_time = models.DateTimeField(blank=True, null=True)
	check_in_time = models.DateTimeField(blank=True, null=True)
	status = models.BooleanField(default=False)

	class Meta:
		abstract = True

	def __str__(self):
		return u'{0}-{1}'.format(self.object, self.owner)

	def check_out(self):
		if not os.path.exists(os.path.dirname(self.epub)):
			os.mkdir(os.path.dirname(self.epub))
		path = self.object.custom_epub_create(self.epub, self.owner)
		path = self.object.custom_txt_create(self.txt, self.owner)
		from utils.epub import remove_blankline
		remove_blankline(path, path)

		self.check_out_time = timezone.now()
		self.check_in_time = self.check_out_time + datetime.timedelta(days=30)
		self.status = True
		self.save()

		return path

	def check_in(self):
		self.check_in_time = timezone.now()
		self.status = False
		self.save()
		try:
			os.remove(self.epub)
			os.remove(self.txt)
		except BaseException as e:
			pass
		return self.epub


class LibraryRecord(Library):
	owner = models.ForeignKey(User,
		on_delete=models.CASCADE,
		related_name='libraryrecord_set')
	object = models.ForeignKey(Book,
		on_delete=models.CASCADE,
		related_name='libraryrecord_set')

	def __init__(self, *args, **kwargs):
		super(Library, self).__init__(*args, **kwargs)
		self.epub = BASE_DIR + u'/file/ebookSystem/library/{0}/{1}{2}.epub'.format(
			self.owner.username, self.id, self.object.book_info.bookname)
		self.txt = BASE_DIR + u'/file/ebookSystem/library/{0}/{1}{2}.txt'.format(
			self.owner.username, self.id, self.object.book_info.bookname)


class Recommend(models.Model):
	content = models.TextField()
	date = models.DateField(default=timezone.now)

	class Meta:
		abstract = True


class EditRecord(models.Model):
	part = models.ForeignKey(EBook,
		blank=True,
		null=True,
		on_delete=models.SET_NULL,
		related_name='editrecord_set')
	CATEGORY = (
		('based', u'初階'),
		(u'advanced', u'進階'),
	)
	category = models.CharField(max_length=10, choices=CATEGORY)
	number_of_times = models.IntegerField()
	editor = models.ForeignKey(User,
		blank=True,
		null=True,
		on_delete=models.SET_NULL,
		related_name='editrecord_set')
	edit = models.TextField()
	finish = models.TextField()
	get_date = models.DateField(blank=True, null=True)
	service_hours = models.IntegerField(default=0)
	stay_hours = models.IntegerField(default=0)
	serviceInfo = models.ForeignKey(ServiceInfo,
		blank=True,
		null=True,
		on_delete=models.SET_NULL,
		related_name='editrecord_set')

	class Meta:
		unique_together = (('part', 'number_of_times'), )

	def __str__(self):
		try:
			return self.part.ISBN_part
		except:
			return str(None)

	def textimport(self):
		self.edit = self.source_text()
		self.finish = ''
		self.save()

	def textexport(self):
		pass

	def record_info(self):
		self.editor = self.part.editor
		self.get_date = self.part.get_date
		self.stay_hours = self.part.service_hours
		self.service_hours = self.compute_service_hours()
		self.save()

	def group_ServiceInfo(self):
		month_ServiceInfo = None
		if self.get_date and self.editor:
			month = datetime.date(year=self.get_date.year,
				month=self.get_date.month,
				day=1)
			try:
				month_ServiceInfo = ServiceInfo.objects.get(user=self.editor,
					date=month)
			except:
				month_ServiceInfo = ServiceInfo.objects.create(
					user=self.editor, date=month)
			self.serviceInfo = month_ServiceInfo
			self.save()
		return month_ServiceInfo

	def compute_service_hours(self):
		service_hours = 0
		for editLog in self.editlog_set.filter(
			user=self.editor).order_by('order'):
			if editLog.edit_count != 0:
				service_hours = service_hours + 1
				continue
			try:
				previous_editLog = self.editlog_set.all().get(
					order=editLog.order - 1)
				if previous_editLog.edit_count != 0:
					service_hours = service_hours + 1
			except:
				continue
		return service_hours

	def source_text(self):
		import_source = self.number_of_times - 1
		if import_source == 0:
			from utils import tag
			source = self.part.get_path()
			try:
				with io.open(source, 'r', encoding='utf-8') as sourceFile:
					content = sourceFile.read()
				return tag.add_tag(content)
			except IOError:
				return ''
		else:
			source = EditRecord.objects.get(part=self.part,
				number_of_times=import_source)
			return source.finish

	def destination_text(self):
		pass

	def diff(self):
		from difflib import SequenceMatcher

		srcSoup = BeautifulSoup(self.source_text(), 'html5lib')
		src_content_text = srcSoup.get_text().replace('\n',
			'').replace('\r', '').replace('   ', '').replace('  ',
			'').replace(u' ', '')

		dstSoup = BeautifulSoup(self.finish, 'html5lib')
		dst_content_text = dstSoup.get_text().replace('\n',
			'').replace('\r', '').replace('   ', '').replace('  ',
			'').replace(u' ', '')

		match = SequenceMatcher(None, src_content_text,
			dst_content_text).get_matching_blocks()
		same_character = 0
		for block in match:
			same_character = same_character + block.size

		return [
			len(match), same_character,
			len(src_content_text),
			len(dst_content_text)
		]

	def edit_distance(self):
		import Levenshtein

		srcSoup = BeautifulSoup(self.source_text(), 'html5lib')
		src_content_text = srcSoup.get_text().replace('\n',
			'').replace('\r', '').replace('   ', '').replace('  ',
			'').replace(u' ', '')

		dstSoup = BeautifulSoup(self.finish, 'html5lib')
		dst_content_text = dstSoup.get_text().replace('\n',
			'').replace('\r', '').replace('   ', '').replace('  ',
			'').replace(u' ', '')

		return Levenshtein.distance(src_content_text, dst_content_text)


class EditLog(models.Model):
	edit_record = models.ForeignKey(EditRecord,
		blank=True,
		null=True,
		on_delete=models.SET_NULL,
		related_name='editlog_set')
	user = models.ForeignKey(User,
		blank=True,
		null=True,
		on_delete=models.SET_NULL,
		related_name='editlog_set')
	time = models.DateTimeField(default=timezone.now)
	order = models.IntegerField()
	edit_count = models.IntegerField()

	def __str__(self):
		return self.edit_record.part.ISBN_part + '-{0}'.format(self.order)


class Category(models.Model):
	name = models.CharField(max_length=255)
	org = models.ForeignKey(
		Organization,
		on_delete=models.CASCADE,
		related_name='category_set',
	)

	def __str__(self):
		return self.name


class IndexCategory(models.Model):
	parent = models.ForeignKey('IndexCategory',
		on_delete=models.CASCADE,
		related_name='child_set',
		blank=True,
		null=True)
	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name

	@property
	def books(self):
		result = []
		result.extend(self.book_set.all())
		for child in self.child_set.all():
			result.extend(child.books)
		return result

	@property
	def descendants_id(self):
		result = []
		result.append(self.id)
		for child in self.child_set.all():
			result.extend(child.descendants_id)
		return result

	@property
	def descendants(self):
		result = []
		for child in self.child_set.all():
			result.append(child.descendants)
		path = []
		node = self
		while node:
			path.append({'id': node.id, 'name': node.name})
			node = node.parent
		path.reverse()

		return {
			'id': self.id,
			'name': self.name,
			'path': path,
			'childs': result,
		}


def add_watermark(self, text, fontname, fontsize, imagefile, output_dir):
	img0 = Image.new("RGBA", (1, 1))
	draw0 = ImageDraw.Draw(img0)
	font = ImageFont.truetype(fontname, fontsize)
	t_width, t_height = draw0.textsize(str(text, 'UTF-8'), font=font)
	img = Image.new("RGBA", (t_width, t_height), (255, 0, 0, 0))
	draw = ImageDraw.Draw(img)
	draw.text((0, 0), str(text, 'UTF-8'), font=font, fill=(0, 255, 255, 128))
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


#===== ISSN Book =====


class ISSNBookInfo(models.Model):
	ISSN = models.CharField(max_length=20, primary_key=True)
	title = models.CharField(max_length=255)
	house = models.CharField(max_length=255)

	def __str__(self):
		return self.title


class ISSNBook(models.Model):
	ISSN_volume = models.CharField(max_length=20, primary_key=True)
	ISSN_book_info = models.ForeignKey(ISSNBookInfo, on_delete=models.CASCADE)
	volume = models.IntegerField()
	date = models.DateField()
	upload_date = models.DateField(default=timezone.now)
	owner = models.ForeignKey(User,
		blank=True,
		null=True,
		on_delete=models.SET_NULL)

	def __init__(self, *args, **kwargs):
		super(ISSNBook, self).__init__(*args, **kwargs)
		self.epub_file = BASE_DIR + '/file/ebookSystem/ISSNBook/{0}/ebook/{0}.epub'.format(
			self.ISSN_volume)

	def __str__(self):
		return self.ISSN_book_info.title + str(self.volume)
