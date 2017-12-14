# coding: utf-8

from rest_framework import filters

class CBCFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		chinese_book_category = request.query_params.get('chinese_book_category')
		if chinese_book_category:
			return queryset.filter(chinese_book_category__startswith=chinese_book_category)
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
		if status:
			return queryset.filter(status=status)
		else:
			return queryset

from genericUser.models import User
class EBookEditorFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		editor_id = request.query_params.get('editor_id')
		if editor_id:
			editor = User.objects.get(id=editor_id)
			return queryset.filter(editor=editor)
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
