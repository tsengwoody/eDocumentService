# coding: utf-8

from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets
from .premissions import *
from .serializers import *

class UserManagerViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	filter_backends = (filters.OrderingFilter, filters.SearchFilter,)
	ordering_fields = ('username',)
	search_fields = ('username', 'email',)
	permission_classes = (IsManager, )

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = (UserIsSelf, )

class AnnouncementViewSet(viewsets.ModelViewSet):
	queryset = Announcement.objects.all()
	serializer_class = AnnouncementSerializer
	filter_backends = (filters.OrderingFilter, filters.SearchFilter,)
	ordering_fields = ('datetime',)
	search_fields = ('category',)
	permission_classes = (IsManagerOrReadOnly, )

class QAndAViewSet(viewsets.ModelViewSet):
	queryset = QAndA.objects.all()
	serializer_class = QAndASerializer
	permission_classes = (IsManagerOrReadOnly, )
