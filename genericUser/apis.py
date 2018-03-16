# coding: utf-8

from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from utils.resource import *
from .filters import *
from .premissions import *
from .serializers import *

class UserViewSet(viewsets.ModelViewSet, ResourceViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = (UserDataPermission, )
	filter_backends = (filters.OrderingFilter, filters.SearchFilter, UserSelfOrManagerFilter,)
	ordering_fields = ('username',)
	search_fields = ('username', 'email',)

	def perform_create(self, serializer):
		instance = serializer.save(
			is_license = True,
			auth_phone = False,
			auth_email = False,
		)
		instance.set_password(self.request.data['password'])
		instance.save()

	def perform_update(self, serializer):
		if self.request.data.has_key('email') or self.request.data.has_key('phone'):
			auth_email = (serializer.validated_data['email'] == serializer.instance.email) & serializer.instance.auth_email
			auth_phone = (serializer.validated_data['phone'] == serializer.instance.phone) & serializer.instance.auth_phone
			serializer.save(auth_email=auth_email, auth_phone=auth_phone)
		else:
			print 'origin'
			serializer.save()


	def get_fullpath(self, obj, dir, resource):
		fullpath = None
		if dir == 'disability_card':
			if resource == 'front':
				fullpath = obj.disability_card_front
			if resource == 'back':
				fullpath = obj.disability_card_back
		return fullpath

	@detail_route(
		methods=['post'],
		url_name='set-password',
		url_path='action/set_password',
	)
	def set_password(self, request, pk=None):
		obj = self.get_object()
		from django.contrib.auth import authenticate
		user = authenticate(username=obj.username, password=self.request.data['old_password'])
		if user is not None and self.request.data['new_password1'] == self.request.data['new_password2']:
			user.set_password(self.request.data['new_password1'])
			user.save()
			return Response(status=status.HTTP_202_ACCEPTED)
		return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

class ServiceInfoViewSet(viewsets.ModelViewSet):
	queryset = ServiceInfo.objects.all()
	serializer_class = ServiceInfoSerializer
	filter_backends = (ServiceInfoUserFilter, ServiceInfoExchangeFilter,)

class ServiceInfoAddViewSet(ServiceInfoViewSet):
	serializer_class = ServiceInfoAddSerializer

class AnnouncementViewSet(viewsets.ModelViewSet):
	queryset = Announcement.objects.all().order_by('-datetime')
	serializer_class = AnnouncementSerializer
	filter_backends = (filters.OrderingFilter, filters.SearchFilter, AnnouncementCategoryFilter, AnnouncementNewestFilter, )
	ordering_fields = ('datetime',)
	search_fields = ('category',)
	permission_classes = (IsManagerOrReadOnly, )

class QAndAViewSet(viewsets.ModelViewSet):
	queryset = QAndA.objects.all()
	serializer_class = QAndASerializer
	permission_classes = (IsManagerOrReadOnly, )

class OrganizationViewSet(viewsets.ModelViewSet):
	queryset = Organization.objects.all()
	serializer_class = OrganizationSerializer
	permission_classes = (IsManagerOrReadOnly, )
