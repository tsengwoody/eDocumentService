# coding: utf-8

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework import filters
from rest_framework import viewsets
from .filters import *
from .serializers import *

class BookViewSet(viewsets.ModelViewSet):
	queryset = Book.objects.all()
	serializer_class = BookSerializer

class EBookViewSet(viewsets.ModelViewSet):
	queryset = EBook.objects.all()
	serializer_class = EBookSerializer
	filter_backends = (EBookStatusFilter, EBookEditorFilter,)

class BookInfoViewSet(viewsets.ModelViewSet):
	queryset = BookInfo.objects.filter(book__status__gte=Book.STATUS['finish']).order_by('-date')
	serializer_class = BookInfoSerializer
	filter_backends = (filters.OrderingFilter, filters.SearchFilter, CBCFilter, NewestFilter, HottestFilter, )
	ordering_fields = ('date',)
	search_fields = ('ISBN', 'bookname', 'author', )

class EditRecordViewSet(viewsets.ModelViewSet):
	queryset = EditRecord.objects.all()
	serializer_class = EditRecordSerializer
	filter_backends = (filters.OrderingFilter, EditRecordEditorFilter, EditRecordServiceInfoFilter,)
	ordering_fields = ('username',)
