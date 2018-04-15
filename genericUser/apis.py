# coding: utf-8

import json
import requests
import urllib
from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from utils.resource import *
from .filters import *
from .premissions import *
from .serializers import *

from django.core.cache import cache
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.template import Context

from mysite.settings import BASE_DIR, SERVICE, MANAGER, OTP_ACCOUNT, OTP_PASSWORD

class UserViewSet(viewsets.ModelViewSet, ResourceViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	#permission_classes = (UserDataPermission, )
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
		if self.request.data.has_key('email'):
			match_email = serializer.validated_data['email'] == serializer.instance.email
		if self.request.data.has_key('phone'):
			match_phone = serializer.validated_data['phone'] == serializer.instance.phone

		if self.request.data.has_key('email'):
			auth_email = match_email & serializer.instance.auth_email
			serializer.save(auth_email=auth_email)
		else:
			serializer.save()

		if self.request.data.has_key('phone'):
			auth_phone = match_phone & serializer.instance.auth_phone
			serializer.save(auth_phone=auth_phone)
		else:
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
		methods=['get', 'post'],
		url_name='verify',
		url_path='action/verify',
	)
	def verify(self, request, pk=None):
		res = {}
		obj = self.get_object()
		if request.POST.has_key('generate') and request.POST['generate'] == 'email':
			if not cache.has_key(obj.email):
				import random
				import string
				vcode = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
				cache.set(obj.email, {'vcode': vcode}, 600)
			else:
				vcode = cache.get(obj.email)['vcode']
			subject = u'[驗證] {0} 信箱驗證碼'.format(obj.username)
			t = get_template('email/email_validate.txt')
			body = t.render(Context(locals()))
			email = EmailMessage(subject=subject, body=body, from_email=SERVICE, to=[obj.email])
			email.send(fail_silently=False)
			res['detail'] = u'已寄送到您的電子信箱'
		elif request.POST.has_key('generate') and request.POST['generate'] == 'phone':
			if not cache.has_key(request.user.phone):
				import random
				import string
				vcode = ''.join(random.choice(string.digits) for _ in range(6))
				cache.set(request.user.phone, {'vcode': vcode}, 600)
			else:
				vcode = cache.get(request.user.phone)['vcode']
			data = u'親愛的{0}您的信箱驗證碼為：{1}，請在10分鐘內輸入。\n'.format(request.user.username, vcode)
			url = 'https://api2.kotsms.com.tw/kotsmsapi-1.php?username={0}&password={1}&dstaddr={2}&smbody={3}'.format(
				OTP_ACCOUNT, OTP_PASSWORD, request.user.phone, urllib.quote(data.encode('big5'))
			)
			session = requests.Session()
			response = session.get(url)
			if response.text.split('=')[1] > 0:
				res['detail'] = u'已寄送到您的手機'
			else:
				res['detail'] = u'請確認手機號碼是否正確或聯絡系統管理員'
				return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)
		elif request.POST.has_key('verification_code') and request.POST.has_key('type') and request.POST['type'] == 'email':
			if not cache.has_key(obj.email):
				res['detail'] = u'驗證碼已過期，請重新產生驗證碼'
				return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)
			input_vcode = request.POST['verification_code']
			vcode = cache.get(obj.email)['vcode']
			if input_vcode == vcode:
				res['detail'] = u'信箱驗證通過'
				obj.auth_email = True
				obj.save()
			else:
				res['detail'] = u'信箱驗證碼不符'
				return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)
		elif request.POST.has_key('verification_code') and request.POST.has_key('type') and request.POST['type'] == 'phone':
			if not cache.has_key(obj.phone):
				res['detail'] = u'驗證碼已過期，請重新產生驗證碼'
				return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)
			input_vcode = request.POST['verification_code']
			vcode = cache.get(obj.phone)['vcode']
			if input_vcode == vcode:
				res['detail'] = u'手機驗證通過'
				obj.auth_phone = True
				obj.save()
			else:
				res['detail'] = u'手機驗證碼不符'
				return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)
		return Response(data=res, status=status.HTTP_202_ACCEPTED)

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
			return Response(data={'detail': u'變更密碼成功'}, status=status.HTTP_202_ACCEPTED)
		return Response(data={'detail': u'變更密碼失敗'}, status=status.HTTP_406_NOT_ACCEPTABLE)

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

class BannerContentViewSet(viewsets.ModelViewSet, ResourceViewSet):
	queryset = BannerContent.objects.all()
	serializer_class = BannerContentSerializer
	permission_classes = (IsManagerOrReadOnly, )

	def perform_create(self, serializer):
		instance = serializer.save(
			order = len(BannerContent.objects.all()),
		)
		instance.save()

	def get_fullpath(self, obj, dir, resource):
		fullpath = None
		if dir == 'cover':
			if resource == 'image':
				fullpath = obj.cover_image
		return fullpath
