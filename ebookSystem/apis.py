# coding: utf-8

from rest_framework import permissions, status
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
	filter_backends = (StatusFilter, BookOwnerFilter, BookBooknameFilter,)
	ordering_fields = ('upload_date',)
	permission_classes = (permissions.IsAuthenticated,)
	#permission_classes = (BookDataPermission, )

	def get_fullpath(self, obj, dir, resource):
		fullpath = None
		if not self.request.user.is_manager:
			return ''
		if dir == 'OCR':
			if resource in ['epub', ]:
				fullpath = obj.path +'/OCR/{0}.{1}'.format(obj.ISBN, resource)
		elif dir == 'source':
			if resource in ['epub', 'txt', 'zip', ]:
				fullpath = obj.path +'/{0}.{1}'.format(obj.ISBN, resource)
		else:
			pass
		return fullpath

	@detail_route(
		methods=['post'],
		url_name='download',
		url_path='action/download',
	)
	def download(self, request, pk=None):
		res = {}
		obj = self.get_object()
		try:
			file_path = obj.zip(request.user, request.POST['password'], request.POST['fileformat'])
		except BaseException as e:
			res['detail'] = u'準備文件失敗： {}'.format(unicode(e))
			return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)

		return self.get_resource(file_path)


	@detail_route(
		methods=['post'],
		url_name='review',
		url_path='action/review',
	)
	def review(self, request, pk=None):
		res = {}

		obj = self.get_object()

		if request.POST['result'] == 'success':
			for part in obj.ebook_set.all():
				part.change_status(1, 'active', category='based')
			BookOrder.refresh()
			res['message'] = u'審核通過文件'
		elif request.POST['result'] == 'error':
			obj.delete()
			res['message'] = u'審核退回文件'
		return Response(data=res, status=status.HTTP_202_ACCEPTED)

	@detail_route(
		methods=['post'],
		url_name='set_priority',
		url_path='action/set_priority',
	)
	def set_priority(self, request, pk=None):
		res = {}
		obj = self.get_object()
		try:
			res['priority'] = priority = int(request.POST['priority'])
			obj.priority = priority
			obj.save()
		except BaseException as e:
			return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)
		return Response(data=res, status=status.HTTP_202_ACCEPTED)

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
			newBook = Book(book_info=newBookInfo, ISBN=request.POST['ISBN'], page_per_part=50)
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
					raise(e)
					res['detail'] = u'建立文件失敗' +str(e)
					return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)

			#建立book object和ebook object
			try:
				newBook = Book(book_info=newBookInfo, ISBN=request.POST['ISBN'])
			except:
				newBook = Book.objects.get(ISBN=request.POST['ISBN'])

			newBook.scaner = request.user
			newBook.owner = request.user
			newBook.source = request.POST['category']
			newBook.finish_date = timezone.now()
			newBook.save()

			ebook = EBook.objects.create(book=newBook, part=1, ISBN_part=request.POST['ISBN'] + '-1', begin_page=-1, end_page=-1)
			ebook.change_status(5, 'final')

			res['detail'] = u'成功建立並上傳文件'
			return Response(data=res, status=status.HTTP_202_ACCEPTED)

class BookAddViewSet(BookViewSet):
	serializer_class = BookAddSerializer

class EBookViewSet(viewsets.ModelViewSet, ResourceViewSet):
	queryset = EBook.objects.all()
	serializer_class = EBookSerializer
	filter_backends = (StatusFilter, EditorFilter,)
	permission_classes = (permissions.IsAuthenticated,)

	@list_route(
		methods=['get', 'post'],
		url_name='service',
		url_path='action/service',
	)
	def service(self, request, pk=None):
		res = {}

		if request.method == 'POST':
			editingPartList = request.user.edit_ebook_set.all().filter(status=EBook.STATUS['edit'])
			GET_MAX_EBOOK = 6
			if len(editingPartList) >= GET_MAX_EBOOK:
				res['detail'] = u'您已有超過{0}段文件，請先校對完成再領取'.format(GET_MAX_EBOOK)
				return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)
			try:
				partialBook = BookOrder.objects.filter(book__status=Book.STATUS['active']).order_by('order')[0].book
			except BaseException as e:
				res['detail'] = u'無文件：{0}'.format(unicode(e))
				return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)
			getPart = partialBook.ebook_set.filter(status=EBook.STATUS['active']).order_by('part')[0]
			getPart.change_status(1, 'edit', user=request.user, deadline=datetime.date.today() +datetime.timedelta(days=5))
			serializer = EBookSerializer(getPart)
			res['data'] = serializer.data
			res['detail'] = u'成功取得文件'
			return Response(data=res, status=status.HTTP_202_ACCEPTED)
		if request.method == 'GET':
			try:
				partialBook = BookOrder.objects.filter(book__status=Book.STATUS['active']).order_by('order')[0].book
			except BaseException as e:
				res['detail'] = u'無文件：{0}'.format(unicode(e))
				return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)
			getPart = partialBook.ebook_set.filter(status=EBook.STATUS['active']).order_by('part')[0]
			serializer = EBookSerializer(getPart)
			res['data'] = serializer.data
			res['detail'] = u'成功取得文件'
			return Response(data=res, status=status.HTTP_202_ACCEPTED)

	@detail_route(
		methods=['post'],
		url_name='onactive',
		url_path='action/onactive',
	)
	def onactive(self, request, pk=None):
		res = {}

		obj = self.get_object()
		try:
			obj.onactive()
			res['detail'] = u'再校對已成功'
		except BaseException as e:
			res['detail'] = u'再校對失敗' +str(e)
			return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)
		res['detail'] = u'成功再校對'
		return Response(data=res, status=status.HTTP_202_ACCEPTED)

	@detail_route(
		methods=['post'],
		url_name='assign',
		url_path='action/assign',
	)
	def assign(self, request, pk=None):
		res = {}

		user = User.objects.get(id=request.POST['id'])
		deadline = request.POST['deadline'].split('-')
		deadline = [ int(v) for v in deadline ]
		deadline = timezone.datetime(deadline[0], deadline[1], deadline[2])

		obj = self.get_object()
		try:
			obj.change_status(1, 'edit', user=user, deadline=deadline)
		except BaseException as e:
			res['detail'] = u'指派失敗' +str(e)
			return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)
		res['detail'] = u'指派已成功'
		return Response(data=res, status=status.HTTP_202_ACCEPTED)

	@detail_route(
		methods=['post'],
		url_name='change_status',
		url_path='action/change_status',
	)
	def change_status(self, request, pk=None):
		res = {}

		obj = self.get_object()
		direction = int(request.data['direction'])
		ebook_status = request.data['status']
		obj.change_status(direction, ebook_status)
		serializer = EBookSerializer(obj)
		res['data'] = serializer.data
		res['detail'] = u'成功取得文件'
		return Response(data=res, status=status.HTTP_202_ACCEPTED)

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
			res['message'] = u'審核通過文件'
		if request.POST['result'] == 'error':
			obj.change_status(-1, 'edit')
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


from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from utils.crawler import *
class BookInfoViewSet(viewsets.ModelViewSet):
	queryset = BookInfo.objects.filter(book__status__gte=Book.STATUS['finish']).order_by('-date')
	serializer_class = BookInfoSerializer
	filter_backends = (filters.OrderingFilter, filters.SearchFilter, CBCFilter, NewestFilter, HottestFilter, BookInfoOwnerFilter,)
	ordering_fields = ('date',)
	search_fields = ('ISBN', 'bookname', 'author', )

	@method_decorator(ensure_csrf_cookie)
	@list_route(
		methods=['post'],
		url_name='isbn2bookinfo',
		url_path='action/isbn2bookinfo',
	)
	def isbn2bookinfo(self, request, pk=None):
		res = {}

		ISBN = request.POST['ISBN']
		if len(ISBN) == 10 and not ISBN10_check(ISBN):
			res['detail'] = u'ISBN10碼錯誤'
			return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)
		if len(ISBN) == 13 and not ISBN13_check(ISBN):
			res['detail'] = u'ISBN13碼錯誤'
			return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)
		if len(ISBN) == 10:
			ISBN = ISBN10_to_ISBN13(ISBN)

		if request.POST['source'] == 'NCL':
			#=====NCL=====
			try:
				res['bookinfo'] = get_ncl_bookinfo(ISBN)
				res['bookinfo']['source'] = 'NCL'
			except BaseException as e:
				res['detail'] = u'NCL 無資料'
				return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)

		elif request.POST['source'] == 'douban':
			#=====douban=====
			try:
				res['bookinfo'] = get_douban_bookinfo(ISBN)
				res['bookinfo']['source'] = 'douban'
			except BaseException as e:
				res['detail'] = u'douban 無資料'
				return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)

		res['message'] = u'成功取得資料'
		return Response(data=res, status=status.HTTP_202_ACCEPTED)

	@list_route(
		methods=['post'],
		url_name='key2bookinfo',
		url_path='action/key2bookinfo',
	)
	def key2bookinfo(self, request, pk=None):
		res = {}

		if request.POST['source'] == 'NCL':
			p_logic = re.compile(r'FO_SchRe1ation(?P<count>\d+)')
			p_field = re.compile(r'FO_SearchField(?P<count>\d+)')
			p_value = re.compile(r'FO_SearchValue(?P<count>\d+)')

			query_dict = {}
			#for k,v in request.POST.iteritems():
			for k,v in request.POST.items():
				search_logic = p_logic.search(k)
				search_field = p_field.search(k)
				search_value = p_value.search(k)
				if search_logic or search_field or search_value:
					query_dict[k] = v

			try:
				res['bookinfo_list'] = get_ncl_bookinfo_list(query_dict)
				for r in res['bookinfo_list']:
					r['source'] = 'NCL'
			except BaseException as e:
				res['detail'] = u'查詢書籍錯誤。{0}'.format(unicode(e))
				return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)

		elif request.POST['source'] == 'douban':
			try:
				res['bookinfo_list'] = get_douban_bookinfo_list(request.POST['search_query'])
				for r in res['bookinfo_list']:
					r['source'] = 'douban'
			except BaseException as e:
				res['detail'] = u'查詢書籍錯誤。{0}'.format(unicode(e))
				return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)

		res['message'] = u'成功取得資料'
		return Response(data=res, status=status.HTTP_202_ACCEPTED)

class BookOrderViewSet(viewsets.ModelViewSet):
	queryset = BookOrder.objects.all()
	serializer_class = BookOrderSerializer
	filter_backends = (filters.OrderingFilter, filters.SearchFilter, )
	search_fields = ('order',)
	permission_classes = (permissions.IsAuthenticated,)

class EditRecordViewSet(viewsets.ModelViewSet):
	queryset = EditRecord.objects.all().order_by('-get_date')
	serializer_class = EditRecordSerializer
	filter_backends = (filters.OrderingFilter, EditorFilter, EditRecordServiceInfoFilter,)
	ordering_fields = ('username',)
	permission_classes = (permissions.IsAuthenticated,)

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

class BookRecommendViewSet(viewsets.ModelViewSet):
	queryset = BookRecommend.objects.all().order_by('-date')
	serializer_class = BookRecommendSerializer

class LibraryRecordViewSet(viewsets.ModelViewSet, ResourceViewSet):
	queryset = LibraryRecord.objects.all()
	serializer_class = LibraryRecordSerializer
	filter_backends = (LibraryRecordUserFilter, LibraryRecordStatusFilter,)
	permission_classes = (permissions.IsAuthenticated, ManagerOrOwner,)

	def get_fullpath(self, obj, dir, resource):
		fullpath = None
		if dir == 'source':
			if resource in ['epub', 'txt', 'zip', ]:
				fullpath = getattr(obj, resource, '')
		return fullpath

	@list_route(
		methods=['post'],
		url_name='check_create',
		url_path='action/check_create',
	)
	def check_create(self, request, pk=None):
		res = {}
		book = Book.objects.get(ISBN=request.POST['ISBN'])
		lr_user = request.user.libraryrecord_set.filter(status=True)
		if len(lr_user) >5:
			res['message'] = u'已到達借閱上限，同時可借閱書量為5本，請先歸還書籍再借閱'
			return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)
		if len(lr_user.filter(object=book)) >0:
			res['message'] = u'已在借閱書櫃無需再借閱'
			return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)

		lr = LibraryRecord.objects.create(owner=request.user, object=book)
		res['id'] = lr.id
		return Response(data=res, status=status.HTTP_202_ACCEPTED)

	@detail_route(
		methods=['post'],
		url_name='check_inout',
		url_path='action/check_inout',
	)
	def check_inout(self, request, pk=None):
		res = {}
		obj = self.get_object()
		if request.POST['action'] == 'check_out':
			obj.check_out()
			return Response(data=res, status=status.HTTP_202_ACCEPTED)
		elif request.POST['action'] == 'check_in':
			obj.check_in()
			return Response(data=res, status=status.HTTP_202_ACCEPTED)

	@detail_route(
		methods=['get', 'post'],
		url_name='download',
		url_path='action/download',
	)
	def download(self, request, pk=None):
		res = {}
		obj = self.get_object()
		if request.method == 'POST':
			from django.contrib.auth import authenticate
			user = authenticate(username=request.user.username, password=request.POST['password'])
			if not user is None:
				from utils.other import get_client_ip
				get_ip = get_client_ip(request)
				GetBookRecord.objects.create(book=obj.object, user=request.user, get_ip=get_ip)
				if request.POST['fileformat'] == 'epub':
					return self.get_resource(obj.epub)
				elif request.POST['fileformat'] == 'txt':
					return self.get_resource(obj.txt)
			else:
				res['detail'] = u'身份認證失敗'
				return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)

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
