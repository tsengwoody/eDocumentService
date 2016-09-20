# coding: utf-8
from django.db import models
from django.utils import timezone
from mysite.settings import BASE_DIR
from genericUser.models import User, ServiceHours
from guest.models import Guest
from account.models import Editor
import glob,os
import datetime
import codecs
import shutil
from PIL import Image, ImageFont, ImageDraw

class BookInfo(models.Model):
	ISBN = models.CharField(max_length=20, primary_key=True)
	bookname = models.CharField(max_length=50)
	author = models.CharField(max_length=50)
	house = models.CharField(max_length=30)
	date = models.DateField()
	def __unicode__(self):
		return self.bookname

class Book(models.Model):
	ISBN = models.CharField(max_length=20, primary_key=True)
	book_info = models.OneToOneField(BookInfo, related_name='book')
	path = models.CharField(max_length=255, blank=True, null=True)
	page_count = models.IntegerField(blank=True, null=True)
	part_count = models.IntegerField(blank=True, null=True)
	page_per_part = models.IntegerField(default=50)
	priority = models.IntegerField(default=0)
	scaner = models.ForeignKey(User,blank=True, null=True, on_delete=models.SET_NULL, related_name='scan_book_set')
	owners = models.ManyToManyField(Guest, related_name='own_book_set')
	upload_date = models.DateField(default = timezone.now)
	status = models.IntegerField(default=0)
	STATUS = {'inactive':0, 'active':1, 'edit':2, 'review':3, 'revise':4, 'finish':5, 'indesignate':6, 'designate':7}
	def __unicode__(self):
		return self.book_info.bookname

	def status_int2str(self):
		for k, v in self.STATUS.iteritems():
			if v == self.status:
				return k
		return 'unknown'

	def create_EBook(self):
		if not (len(self.ebook_set.all()) == 0 and self.validate_folder()):
			return False
		for i in range(self.part_count):
			begin_page = i*self.page_per_part
			end_page = (i+1)*self.page_per_part-1
			if end_page >= self.page_count:
				end_page = self.page_count-1
			ISBN_part = self.ISBN + '-{0}'.format(i+1)
			EBook.objects.create(book=self, part=i+1, ISBN_part=ISBN_part, begin_page=begin_page, end_page=end_page)
		for ebook in self.ebook_set.all():
			ebook.add_tag()
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

	def zip(self, password):
		import pyminizip
#		import zipfile
		zip_file_name = self.path +'/OCR/' +self.ISBN +'.zip'
		zip_list = [ file.get_path('-clean') for file in self.ebook_set.all() ]
		try:
			pyminizip.compress_multiple(zip_list, zip_file_name, password, 5)
			return zip_file_name
		except:
			os.remove(zip_file_name)
			return ''
#		zf = zipfile.ZipFile(zip_file_name, "w", zipfile.zlib.DEFLATED)
#		try:
#			for i in range(self.part_count):
#				tar = self.path +'/OCR/' +'part{0}-edit.txt'.format(i+1)
#				arcname = 'part{0}-edit.txt'.format(i+1)
#				zf.write(tar, arcname)
#		except:
#			pass
#			shutil.rmtree(zip_file_name)
#		zf.close()

	def collect_is_finish(self):
		is_finish = True
		for part in self.ebook_set.all():
			is_finish = is_finish and part.status == part.STATUS['finish']
		return is_finish

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
	editor = models.ForeignKey(Editor,blank=True, null=True, on_delete=models.SET_NULL, related_name='edit_ebook_set')
	finish_date = models.DateField(blank=True, null=True)
	deadline = models.DateField(blank=True, null=True)
	get_date = models.DateField(blank=True, null=True)
	service_hours = models.IntegerField(default=0)
	serviceHours = models.ForeignKey(ServiceHours,blank=True, null=True, on_delete=models.SET_NULL)
	status = models.IntegerField(default=1)
	STATUS = {'inactive':0, 'active':1, 'edit':2, 'review':3, 'finish':4, 'sc_active':5, 'sc_edit':6, 'sc_finish':7}
	sc_editor = models.ForeignKey(Editor,blank=True, null=True, on_delete=models.SET_NULL, related_name='sc_edit_ebook_set')
	sc_finish_date = models.DateField(blank=True, null=True)
	sc_deadline = models.DateField(blank=True, null=True)
	sc_get_date = models.DateField(blank=True, null=True)

	def status_int2str(self):
		for k, v in self.STATUS.iteritems():
			if v == self.status:
				return k
		return 'unknown'

	def get_path(self, string=''):
		if string == '-final' or string == '-clean':
			return self.book.path +'/OCR/part{0}{1}.html'.format(self.part, string)
		else:
			return self.book.path +'/OCR/part{0}{1}.txt'.format(self.part, string)

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
		return self.book.book_info.bookname+u'-part'+str(self.part)

	def get_content(self, action='', encoding='utf-8'):
		filePath = self.get_path(action)
		with codecs.open(filePath, 'r', encoding=encoding) as sourceFile:
			source_content = sourceFile.read()
		file_head = source_content[0]
		source_content = source_content[1:]
		return [source_content,file_head]

	def set_content(self, finish_content, edit_content, encoding='utf-8', fileHead = u'\ufeff'):
		finishFilePath = self.get_path('-finish')
		editFilePath = self.get_path('-edit')
		with codecs.open(finishFilePath, 'a', encoding=encoding) as fileWrite:
			fileWrite.write(finish_content)
		with codecs.open(editFilePath, 'w', encoding=encoding) as fileWrite:
			fileWrite.write(fileHead+edit_content)
		return True

	def load_full_content(self, fileHead = u'\ufeff'):
		edit_content = self.get_content('-edit')[0]
		finish_content = self.get_content('-finish')[0]
		self.set_content('', finish_content +edit_content)
		with codecs.open(self.get_path('-finish'), 'w', encoding='utf-8') as finishFile:
			finishFile.write(u'\ufeff')
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
	    print output_dir+" "+imagefile + " saved..."
	    img2.save(output_dir + imagefile)
	    del draw0, draw
	    del img0, img, img2

	def get_html(self):
		html_path = BASE_DIR +u'/static/ebookSystem/document/{0}/OCR'.format(self.book.book_info.ISBN)
		if not os.path.exists(html_path):
			os.makedirs(html_path)
		shutil.copyfile(self.get_path('-clean'), html_path +'/part{0}-final.html'.format(self.part))
		default_page_url = html_path +'/part{0}-final.html'.format(self.part)
		default_page_url = default_page_url.replace(BASE_DIR +'/static/', '')
		return default_page_url

	def add_tag(self, encoding='utf-8'):
		source = self.get_path()
		destination = self.get_path('-edit')
		from utils import tag
		tag.add_tag(source, destination)

	def clean_tag(self, template='book_template.html', encoding='utf-8'):
		source = self.get_path('-finish')
		destination = self.get_path('-clean')
		template = BASE_DIR +u'/templates/' +template
		from utils import tag
		tag.add_template_tag(source, destination, template)
		title = self.book.book_info.bookname +'-part{0}'.format(self.part)
		tag.clean_tag(destination, destination, title)

	def create_SpecialContent(self, encoding='utf-8'):
		org_path = BASE_DIR +u'/static/ebookSystem/document/{0}/source/{1}'.format(self.book.book_info.ISBN, "org")
		source_path = self.book.path +u'/source'
		fileList=os.listdir(source_path)
		fileList = sorted(fileList)
		scanPageList=[scanPage for scanPage in fileList if scanPage.split('.')[-1].lower() == 'jpg']
		scanPageList = scanPageList[self.begin_page:self.end_page+1]
		source = self.get_path('-clean')
		with codecs.open(source, 'r', encoding=encoding) as sourceFile:
			source_content = sourceFile.read()
		file_head = source_content[0]
		source_content = source_content[1:]
		from bs4 import BeautifulSoup, NavigableString
		soup = BeautifulSoup(source_content, 'lxml')
		span_tags = soup.find_all('span')
		for span_tag in span_tags:
			if span_tag.attrs.has_key('class') and ('unknown' in span_tag.attrs['class'] or 'mathml' in span_tag.attrs['class']):
				p_tag_count = 0
				for parent in span_tag.parents:
					if parent.name == 'p':
						span_tag_pparent = parent
						p_tag_count = p_tag_count +1
				if p_tag_count != 1:continue
				try:
					tag_id = span_tag_pparent['id']
					page = scanPageList.index(span_tag['id'])
				except:
					continue
				id = self.ISBN_part +'-' +tag_id
				content = str(span_tag_pparent)
				if 'unknown' in span_tag.attrs['class']:
					type = SpecialContent.TYPE['unknown']
				elif 'mathml' in span_tag.attrs['class']:
					type = SpecialContent.TYPE['mathml']
				else:
					continue
				try:
					SpecialContent.objects.get(id=id)
				except:
					SpecialContent.objects.create(id=id, ebook=self, tag_id=tag_id, page=page, content=content, type=type)
		img_tags = soup.find_all('img')
		for img_tag in img_tags:
			if not img_tag.attrs.has_key('src'):
				p_tag_count = 0
				for parent in img_tag.parents:
					if parent.name == 'p':
						img_tag_pparent = parent
						p_tag_count = p_tag_count +1
				if p_tag_count != 1:continue
				try:
					tag_id = img_tag_pparent['id']
					page = scanPageList.index(img_tag['id'])
				except:
					continue
				id = self.ISBN_part +'-' +tag_id
				content = str(img_tag_pparent)
				type = SpecialContent.TYPE['image']
				try:
					SpecialContent.objects.get(id=id)
				except:
					SpecialContent.objects.create(id=id, ebook=self, tag_id=tag_id, page=page, content=content, type=type)

	def collect_service_hours(self):
		service_hours = 0
		for sc in self.specialcontent_set.all():
			service_hours = service_hours + sc.service_hours
		return 		service_hours

	def finish_specialcontent_count(self):
		finish_specialcontent_count = 0
		for sc in self.specialcontent_set.all():
			finish_specialcontent_count = finish_specialcontent_count + (sc.status==sc.STATUS['finish'])
		return finish_specialcontent_count

	def specialcontent_count(self):
		return len(self.specialcontent_set.all())

	def zip(self, password):
		import pyminizip
		zip_file_name = self.book.path +'/OCR/' +self.ISBN_part +'.zip'
		zip_list = [self.get_path('-clean')]
		try:
			pyminizip.compress_multiple(zip_list, zip_file_name, password, 5)
			return zip_file_name
		except:
			os.remove(zip_file_name)
			return ''

	def edit_distance(self, src, dst, encoding='utf-8'):
		import Levenshtein
		from bs4 import BeautifulSoup
		with codecs.open(src, 'r', encoding=encoding) as srcFile:
			src_content = srcFile.read()
		srcSoup = BeautifulSoup(src_content, 'lxml')
		src_content_text = srcSoup.get_text().replace('\n', '').replace('\r', '').replace('   ', '').replace('  ', '').replace(u' ', '')
		with codecs.open(dst, 'r', encoding=encoding) as dstFile:
			dst_content = dstFile.read()
		dstSoup = BeautifulSoup(dst_content, 'lxml')
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

class SpecialContent(models.Model):
	id = models.CharField(max_length=30, primary_key=True)
	ebook = models.ForeignKey(EBook, on_delete=models.CASCADE)
	tag_id = models.CharField(max_length=10)
	page = models.IntegerField()
	content = models.TextField()
	service_hours = models.IntegerField(default=0)
	serviceHours = models.ForeignKey(ServiceHours,blank=True, null=True, on_delete=models.SET_NULL)
	status = models.IntegerField(default=0)
	STATUS = {'active':0, 'edit':1, 'finish':2}
	type = models.IntegerField()
	TYPE = {'image':0, 'unknown':1, 'mathml':2}

	def __unicode__(self):
		return self.id

	def status_int2str(self):
		for k, v in self.STATUS.iteritems():
			if v == self.status:
				return k
		return 'unknown'

	def type_int2str(self):
		for k, v in self.TYPE.iteritems():
			if v == self.type:
				return k
		return 'unknown'

	def get_url(self):
		return '/ebookSystem/advanced/edit_{0}/{1}'.format(self.type_int2str(), self.id)


class ReviseContentAction(models.Model):
	from ebookSystem.models import EBook
	ebook = models.ForeignKey(EBook)
	content = models.CharField(max_length=1000)

class ApplyDocumentAction(models.Model):
	from genericUser.models import Center
	book_info = models.ForeignKey(BookInfo)
	center = models.ForeignKey(Center, blank=True, null=True)