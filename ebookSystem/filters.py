# coding: utf-8

from rest_framework import filters

class BaseFilter(filters.BaseFilterBackend):
	key = ''
	type = str
	attr = ''
	def filter_queryset(self, request, queryset, view):
		value = request.query_params.get(self.key)
		if not value:
			return queryset
		try:
			self.value = self.type(value)
			kwargs = {
				self.attr: self.value,
			}
			return queryset.filter(**kwargs)
		except:
			return queryset

# ['book_review_list', 'book_manager', 'book_person', 'ebook_review_list', 'service', ]
class StatusFilter(BaseFilter):
	key = 'status'
	type = int
	attr = 'status'

# ['book_person', ]
class BookOwnerFilter(BaseFilter):
	key = 'owner_id'
	type = str
	attr = 'owner_id'

# ['service', ]
class EditorFilter(BaseFilter):
	key = 'editor_id'
	type = str
	attr = 'editor_id'

# ['book_person', ]
class BookInfoOwnerFilter(BaseFilter):
	key = 'owner_id'
	type = str
	attr = 'book__owner_id'

class BookBooknameFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		bookname = request.query_params.get('bookname')
		if bookname and not bookname=='':
			return queryset.filter(book_info__bookname__contains=bookname)
		else:
			return queryset

class CBCFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		from django.db.models import Q
		try:
			chinese_book_category = int(request.query_params.get('chinese_book_category'))
		except:
			chinese_book_category = -1
		if chinese_book_category >= 0 and chinese_book_category <10:
			CBC = chinese_book_category*100
			return queryset.filter(chinese_book_category__gt=CBC-1, chinese_book_category__lt=CBC+100)
		else:
			return queryset

class NewestFilter(filters.BaseFilterBackend):

	def filter_queryset(self, request, queryset, view):
		newest = request.query_params.get('newest')
		if newest:
			return queryset.order_by('-book__finish_date', '-date')[0:int(newest)]
		else:
			return queryset

class HottestFilter(filters.BaseFilterBackend):

	def filter_queryset(self, request, queryset, view):
		hottest = request.query_params.get('hottest')
		if hottest:
			import datetime
			from django.db.models import Count
			from django.utils import timezone
			from ebookSystem.models import Book, GetBookRecord
			begin_day = timezone.now() -datetime.timedelta(days=30)
			end_day = timezone.now()
			r = GetBookRecord.objects.filter(get_time__gt=begin_day, get_time__lt=end_day).values('book').annotate(count=Count('book'))
			import heapq
			hottest_ISBN = heapq.nlargest(int(hottest), r, key=lambda s: s['count'])
			book_list = [Book.objects.get(ISBN=i['book']) for i in hottest_ISBN ]
			return queryset.filter(book__in=book_list)
		else:
			return queryset

from genericUser.models import User

class EditRecordEditorFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		editor_id = request.query_params.get('editor_id')
		if editor_id:
			editor = User.objects.get(id=editor_id)
			return queryset.filter(editor=editor)
		else:
			return queryset

class EditRecordServiceInfoFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		exchange = request.query_params.get('exchange')
		if exchange and exchange in ['true', 'True']:
			return queryset.exclude(serviceInfo=None)
		elif exchange and exchange in ['false', 'False']:
			return queryset.filter(serviceInfo=None)
		else:
			return queryset

class LibraryRecordUserFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		user_id = request.query_params.get('user_id')
		if user_id:
			user = User.objects.get(id=user_id)
			return queryset.filter(owner=user)
		else:
			return queryset

class LibraryRecordStatusFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		status = request.query_params.get('status')
		if status and status in ['true', 'True']:
			return queryset.filter(status=True)
		elif status and status in ['false', 'False']:
			return queryset.filter(status=False)
		else:
			return queryset
