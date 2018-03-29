# coding: utf-8

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import detail_route
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
	permission_classes = (BookDataPermission, )

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

class EBookViewSet(viewsets.ModelViewSet, ResourceViewSet):
	queryset = EBook.objects.all()
	serializer_class = EBookSerializer
	filter_backends = (EBookStatusFilter, EBookEditorFilter,)

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
