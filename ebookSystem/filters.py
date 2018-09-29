# coding: utf-8

from rest_framework import filters

class BookStatusFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		status = request.query_params.get('status')
		try:
			if status:
				return queryset.filter(status=int(status))
			else:
				return queryset
		except:
			return queryset

class BookOwnerFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		owner_id = request.query_params.get('owner_id')
		if owner_id:
			owner = User.objects.get(id=owner_id)
			return queryset.filter(owner=owner)
		else:
			return queryset

class BookBooknameFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		bookname = request.query_params.get('bookname')
		if bookname and not bookname=='':
			return queryset.filter(book_info__bookname__contains=bookname)
		else:
			return queryset

class BookInfoOwnerFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		value = request.query_params.get('owner_id')
		if value:
			obj = User.objects.get(id=value)
			return queryset.filter(book__owner=obj)
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

class EBookStatusFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		status = request.query_params.get('status')
		try:
			if status:
				return queryset.filter(status=int(status))
			else:
				return queryset
		except:
			return queryset

from genericUser.models import User
class EBookEditorFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		user_id = request.query_params.get('editor_id')
		if user_id:
			user = User.objects.get(id=user_id)
			return queryset.filter(editor=user)
		else:
			return queryset

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
			return queryset.filter(user=user)
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
