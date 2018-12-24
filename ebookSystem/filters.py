# coding: utf-8

from rest_framework import filters
from utils.filters import convert_bool, convert_unicode, KeyMapAttrFilterFactory

# ['book_review_list', 'book_manager', 'book_person', 'ebook_review_list', 'service', ]
StatusFilter = KeyMapAttrFilterFactory(key = 'status', type = int, attr = 'status')

# ['book_shelf']
BoolStatusFilter = KeyMapAttrFilterFactory(key = 'status', type = convert_bool, attr = 'status')

# ['book_person', book_shelf ,]
OwnerFilter = KeyMapAttrFilterFactory(key = 'owner_id', type = str, attr = 'owner_id')

# ['school',]
OrgFilter = KeyMapAttrFilterFactory(key = 'org_id', type = str, attr = 'org_id')

# 
EbookOrgFilter = KeyMapAttrFilterFactory(key = 'org_id', type = str, attr = 'book__org_id')

# ['service', 'serviceinfo_record', ]
EditorFilter = KeyMapAttrFilterFactory(key = 'editor_id', type = str, attr = 'editor_id')

# ['book_person', ]
BookInfoOwnerFilter = KeyMapAttrFilterFactory(key = 'owner_id', type = str, attr = 'book__owner_id')

#['book_manager']
BooknameFilter = KeyMapAttrFilterFactory(key = 'bookname', type = convert_unicode, attr = 'book_info__bookname')

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

class EditRecordServiceInfoFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		exchange = request.query_params.get('exchange')
		if exchange and exchange in ['true', 'True']:
			return queryset.exclude(serviceInfo=None)
		elif exchange and exchange in ['false', 'False']:
			return queryset.filter(serviceInfo=None)
		else:
			return queryset
