# coding: utf-8

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework import filters
from rest_framework import viewsets
from .filters import *
from .premissions import *
from .serializers import *
from utils.resource import *

class BookViewSet(viewsets.ModelViewSet, ResourceViewSet):
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	filter_backends = (BookStatusFilter, BookOwnerFilter,)
	#permission_classes = (BookDataPermission, )

	def get_fullpath(self, obj, dir, resource):
		fullpath = None
		if dir == 'OCR':
			if resource in ['epub', ]:
				fullpath = obj.path +'/OCR/{0}.{1}'.format(obj.ISBN, resource)
		elif dir == 'source':
			if resource in ['epub', 'txt', 'zip', ]:
				fullpath = obj.path +'/{0}.{1}'.format(obj.ISBN, resource)
		else:
			pass
		return fullpath

	@list_route(
		methods=['post'],
		url_name='upload_self',
		url_path='action/create',
	)
	def upload_self(self, request, pk=None):
		res = {}

		if request.method == 'POST':
			#book info 設定
			try:
				newBookInfo = BookInfo.objects.get(ISBN=request.POST['ISBN'])
			except:
				serializer = BookInfoSerializer(data=request.data)
				if not serializer.is_valid():
					res['detail'] = u'序列化驗證失敗' + unicode(serializer.errors)
					return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)
				newBookInfo = serializer.save()

			try:
				book = Book.objects.get(ISBN=request.POST['ISBN'])
				res['detail'] = u'文件已存在'
				return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)
			except:
				pass

			#上傳文件設定
			uploadPath = BASE_DIR + u'/file/ebookSystem/document/{0}'.format(request.POST['ISBN'])
			uploadFilePath = os.path.join(uploadPath, request.POST['ISBN'] +'.zip')
			self.post_resource(uploadFilePath, request.FILES['fileObject'])

			#壓縮文件測試
			try:
				from zipfile import ZipFile
				with ZipFile(uploadFilePath, 'r') as uploadFile:
					uploadFile.testzip()
					uploadFile.extractall(uploadPath)
			except:
				shutil.rmtree(uploadPath)
				res['detail'] = u'非正確ZIP文件'
				return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)

			#資料夾檢查
			from utils import validate
			try:
				validate.validate_folder(
					os.path.join(uploadPath, 'OCR'),
					os.path.join(uploadPath, 'source'),
					50
				)
			except BaseException as e:
				shutil.rmtree(uploadPath)
				res['detail'] = u'上傳壓縮文件結構錯誤，詳細結構請參考說明頁面'
				return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)

			#建立book object
			newBook = Book(book_info=newBookInfo, ISBN=request.POST['ISBN'], path=uploadPath, page_per_part=50)
			try:
				newBook.set_page_count()
			except:
				shutil.rmtree(uploadPath)
				res['detail'] = u'set_page_count error'
				return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)

			newBook.scaner = request.user
			newBook.owner = request.user
			newBook.source = 'self'
			newBook.save()
			try:
				newBook.create_EBook()
			except BaseException as e:
				newBook.delete()
				res['detail'] = u'建立分段失敗'
				return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)

			event = Event.objects.create(creater=request.user, action=newBook)

			res['detail'] = u'成功建立並上傳文件'
			return Response(data=res, status=status.HTTP_202_ACCEPTED)

	@list_route(
		methods=['post'],
		url_name='upload',
		url_path='action/upload',
	)
	def upload(self, request, pk=None):
		res = {}

		if request.method == 'POST':
			#book info 設定
			try:
				newBookInfo = BookInfo.objects.get(ISBN=request.POST['ISBN'])
			except:
				serializer = BookInfoSerializer(data=request.data)
				if not serializer.is_valid():
					res['detail'] = u'序列化驗證失敗' + unicode(serializer.errors)
					return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)
				newBookInfo = serializer.save()

			#判斷是否上傳
			source_priority = {
				'self': 0,
				'txt': 1,
				'epub': 2,
			}
			try:
				book = Book.objects.get(ISBN=request.POST['ISBN'])
				if source_priority[request.POST['category']] <= source_priority[book.source]:
					res['detail'] = u'文件已存在'
					return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)
			except:
				pass

			#上傳文件設定
			uploadPath = BASE_DIR + u'/file/ebookSystem/document/{0}'.format(request.POST['ISBN'])
			uploadFilePath = os.path.join(uploadPath, request.POST['ISBN'] +'.' +request.POST['category'])
			self.post_resource(uploadFilePath, request.FILES['fileObject'])

			#根據選擇上傳格式作業
			final_file = os.path.join(uploadPath, 'OCR') + '/{0}.epub'.format(request.POST['ISBN'], )
			#txt
			if request.POST['category'] == 'txt':
				from ebooklib import epub
				from utils.epub import txt2epub
				try:
					os.makedirs(os.path.dirname(final_file))
					info = {
						'ISBN': newBookInfo.ISBN,
						'bookname': newBookInfo.bookname,
						'author': newBookInfo.author,
						'date': str(newBookInfo.date),
						'house': newBookInfo.house,
						'language': 'zh',
					}
					txt2epub(uploadFilePath, final_file, **info)
				except BaseException as e:
					shutil.rmtree(uploadPath)
					res['detail'] = u'建立文件失敗' +str(e)
					return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)

			#epub
			if request.POST['category'] == 'epub':
				from ebooklib import epub
				from utils.epub import through, add_bookinfo
				try:
					os.makedirs(os.path.dirname(final_file))
					through(uploadFilePath, final_file)
					book = epub.read_epub(final_file)
					book = add_bookinfo(
						book,
						ISBN = newBookInfo.ISBN,
						bookname = newBookInfo.bookname,
						author = newBookInfo.author,
						date = str(newBookInfo.date),
						house = newBookInfo.house,
						language = 'zh',
					)
					epub.write_epub(final_file, book, {})
				except BaseException as e:
					shutil.rmtree(uploadPath)
					res['detail'] = u'建立文件失敗' +str(e)
					return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)

			#建立book object和ebook object
			try:
				newBook = Book(book_info=newBookInfo, ISBN=request.POST['ISBN'], path=uploadPath)
			except:
				newBook = Book.objects.get(ISBN=request.POST['ISBN'])

			newBook.scaner = request.user
			newBook.owner = request.user
			newBook.source = request.POST['category']
			newBook.finish_date = timezone.now()
			newBook.save()

			ebook = EBook.objects.create(book=newBook, part=1, ISBN_part=request.POST['ISBN'] + '-1', begin_page=-1, end_page=-1)
			ebook.change_status(9, 'final')

			res['detail'] = u'成功建立並上傳文件'
			return Response(data=res, status=status.HTTP_202_ACCEPTED)

class EBookViewSet(viewsets.ModelViewSet, ResourceViewSet):
	queryset = EBook.objects.all()
	serializer_class = EBookSerializer
	filter_backends = (EBookStatusFilter, EBookEditorFilter,)

	@detail_route(
		methods=['get', 'post'],
		url_name='edit',
		url_path='action/edit',
	)
	def edit(self, request, pk=None):
		res = {}

		obj = self.get_object()
		if request.method == 'POST':
			content = request.POST['edit']
			origin_finish = request.POST['finish']
			page = request.POST['page']
			if request.POST['type'] == 'save':
				try:
					finishContent, editContent = obj.split_content(content)
					if finishContent == '' or editContent == '':
						raise SystemError('save mark error')
				except BaseException as e:
					res['detail'] = u'標記位置錯誤或有多個標記'
					res['detail'] = unicode(e)
					return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)

				finishContent = origin_finish + finishContent
				obj.set_content(finish_content=finishContent, edit_content=editContent)
				obj.edited_page=int(page)
				obj.save()
				res['detail'] = u'您上次儲存時間為：{0}，請定時存檔喔~'.format(timezone.now())

			elif request.POST['type'] == 'finish':
				finishContent = origin_finish + content
				obj.set_content(finish_content=finishContent, edit_content='')
				obj.change_status(1, 'review')
				event = Event.objects.create(creater=request.user, action=obj)
				res['detail'] = u'完成文件校對，將進入審核'
			elif request.POST['type'] == 'load':
				obj.load_full_content()
				res['detail'] = u'成功載入全部文件內容'
			res['finish'], res['edit'] = obj.get_content()
			res['edited_page'] = obj.edited_page
			return Response(data=res, status=status.HTTP_202_ACCEPTED)
		if request.method == 'GET':
			res['finish'], res['edit'] = obj.get_content()
			res['edited_page'] = obj.edited_page
			return Response(data=res, status=status.HTTP_202_ACCEPTED)

	@detail_route(
		methods=['post'],
		url_name='review',
		url_path='action/review',
	)
	def review(self, request, pk=None):
		res = {}
		obj = self.get_object()
		if not int(request.POST['number_of_times']) == obj.number_of_times:
			res['detail'] = u'校對次數資訊不符'
			return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)
		if request.POST['result'] == 'success':
			obj.change_status(1, 'finish')
			for event in events:
				event.response(status='success', message=u'', user=request.user)
			res['message'] = u'審核通過文件'
		if request.POST['result'] == 'error':
			obj.change_status(-1, 'edit')
			for event in events:
				event.response(status='error', message=u'', user=request.user)
			res['message'] = u'審核退回文件'
		return Response(data=res, status=status.HTTP_202_ACCEPTED)

	def get_fullpath(self, ebook, dir, resource):
		fullpath = None
		if dir == 'OCR':
			if resource == 'origin':
				fullpath = ebook.get_path()
			else:
				fullpath = ebook.get_path('-' +resource)
		elif dir == 'source':
			fullpath = os.path.join(ebook.book.path +u'/source', ebook.get_source_list()[int(resource)])
		else:
			pass
		return fullpath

class BookInfoViewSet(viewsets.ModelViewSet):
	queryset = BookInfo.objects.filter(book__status__gte=Book.STATUS['finish']).order_by('-date')
	serializer_class = BookInfoSerializer
	filter_backends = (filters.OrderingFilter, filters.SearchFilter, CBCFilter, NewestFilter, HottestFilter, BookInfoOwnerFilter,)
	ordering_fields = ('date',)
	search_fields = ('ISBN', 'bookname', 'author', )

class EditRecordViewSet(viewsets.ModelViewSet):
	queryset = EditRecord.objects.all()
	serializer_class = EditRecordSerializer
	filter_backends = (filters.OrderingFilter, EditRecordEditorFilter, EditRecordServiceInfoFilter,)
	ordering_fields = ('username',)

	@detail_route(
		methods=['get', ],
		url_name='analysis',
		url_path='action/analysis',
	)
	def analysis(self, request, pk=None):
		res = {}

		obj = self.get_object()
		[res['len_block'], res['same_character'], res['src_count'], res['dst_count']] = obj.diff()
		res['edit_distance'] = obj.edit_distance()
		res['delete_count'] = res['src_count'] -res['same_character']
		res['insert_count'] = res['dst_count'] -res['same_character']
		res['diff_count'] = res['dst_count'] -res['src_count']
		return Response(data=res, status=status.HTTP_202_ACCEPTED)

#===== ISSN Book =====

class ISSNBookInfoViewSet(viewsets.ModelViewSet):
	queryset = ISSNBookInfo.objects.all()
	serializer_class = ISSNBookInfoSerializer
	filter_backends = (filters.OrderingFilter, filters.SearchFilter, )
	search_fields = ('ISSN', 'title', )

class ISSNBookViewSet(viewsets.ModelViewSet, ResourceViewSet):
	queryset = ISSNBook.objects.all().order_by('-date')
	serializer_class = ISSNBookSerializer
	filter_backends = (filters.OrderingFilter, filters.SearchFilter, )
	ordering_fields = ('volume',)
	@list_route(
		methods=['post'],
		url_name='upload',
		url_path='action/upload',
	)
	def upload(self, request, pk=None):
		res = {}

		if request.method == 'POST':
			serializer = ISSNBookSerializer(data=request.data)
			if not serializer.is_valid():
				res['detail'] = u'序列化驗證失敗' + unicode(serializer.errors)
				return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)
			instance = serializer.save()

			try:
				self.post_resource(instance.epub_file, request.FILES['fileObject'])
			except:
				instance.delete()

			res['detail'] = u'成功建立並上傳文件'
			return Response(data=res, status=status.HTTP_202_ACCEPTED)
