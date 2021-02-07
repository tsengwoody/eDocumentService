﻿# coding: utf-8

import json
import requests
import sys

from django.core.cache import cache
from django.core.mail import EmailMessage
from django.template.loader import get_template

from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny

from django_filters import rest_framework as dffilters

from utils.resource import *
from utils.apis import MixedPermissionModelViewSet
from utils.filters import OwnerOrgManagerFilter
from utils.filters import IsManageObjectPermissionFilterFactory
from utils.permissions import RuleORPermissionFactory
from .filters import *
from .serializers import *

from mysite.settings import BASE_DIR, SERVICE, MANAGER, OTP_ACCOUNT, OTP_PASSWORD


class UserViewSet(viewsets.ModelViewSet, ResourceViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	filter_backends = (
		filters.OrderingFilter,
		filters.SearchFilter,
		dffilters.DjangoFilterBackend,
		IsManageObjectPermissionFilterFactory('self'),
		OrgFilter,
		UserRoleFilter,
		UserAuthFilter,
	)
	ordering_fields = ('username')
	search_fields = (
		'username',
		'email',
		'first_name',
		'last_name',
	)
	filterset_fields = ('is_hot', )

	def perform_create(self, serializer):
		instance = serializer.save(
			is_active=True,
			is_license=True,
			auth_phone=False,
			auth_email=False,
		)
		instance.set_password(self.request.data['password'])
		instance.save()

	def perform_update(self, serializer):

		# 要分開先判斷是否與原始資料相同，再一併存檔
		if 'email' in self.request.data:
			match_email = serializer.validated_data[
				'email'] == serializer.instance.email
			auth_email = match_email & serializer.instance.auth_email
		if 'phone' in self.request.data:
			match_phone = serializer.validated_data[
				'phone'] == serializer.instance.phone
			auth_phone = match_phone & serializer.instance.auth_phone
		if 'org' in self.request.data:
			match_org = serializer.validated_data[
				'org'] == serializer.instance.org
			is_manager = match_org & serializer.instance.is_manager

		if 'email' in self.request.data:
			serializer.save(auth_email=auth_email)
		if 'phone' in self.request.data:
			serializer.save(auth_phone=auth_phone)
		if 'org' in self.request.data:
			serializer.save(is_manager=is_manager)

		serializer.save()

	def get_fullpath(self, obj, dir, resource):
		fullpath = None
		if dir == 'disability_card':
			if resource == 'front':
				fullpath = obj.disability_card_front
			if resource == 'back':
				fullpath = obj.disability_card_back
		return fullpath

	@action(
		detail=False,
		methods=['post'],
		permission_classes=[
		AllowAny,
		],
		url_name='authenticate',
		url_path='action/authenticate',
	)
	def authenticate(self, request, pk=None):
		res = {}

		from django.contrib.auth import authenticate as auth
		user = auth(username=request.data['username'],
			password=request.data['password'])
		if user is None:
			res['detail'] = u'失敗使用者驗證'
			return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)
		else:
			return Response(data=res, status=status.HTTP_202_ACCEPTED)

	@action(
		detail=False,
		methods=['post', 'get'],
		permission_classes=[
		AllowAny,
		],
		url_name='login',
		url_path='action/login',
	)
	def login(self, request, pk=None):
		res = {}

		from django.contrib.auth import (
			login as auth_login,
			logout as auth_logout,
			update_session_auth_hash,
			authenticate,
		)
		user = authenticate(username=request.data['username'],
			password=request.data['password'])
		if user is None:
			res['detail'] = u'帳號或密碼錯誤，請確認輸入的帳號密碼'
			return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)

		auth_login(request, user)
		from django.contrib.sessions.models import Session
		for session in Session.objects.all():
			try:
				if int(
					session.get_decoded()['_auth_user_id']
				) == request.user.id and request.user.username != 'root':
					session.delete()
			except:
				pass
		res['detail'] = u'成功登錄平台'
		return Response(data=res, status=status.HTTP_202_ACCEPTED)

	@action(
		detail=False,
		methods=['post', 'get'],
		permission_classes=[
		AllowAny,
		],
		url_name='logout',
		url_path='action/logout',
	)
	def logout(self, request, pk=None):
		res = {}

		from django.contrib.auth import (
			login as auth_login,
			logout as auth_logout,
			update_session_auth_hash,
			authenticate,
		)
		auth_logout(request)
		res['detail'] = u'成功登出平台'
		return Response(data=res, status=status.HTTP_202_ACCEPTED)

	@action(
		detail=False,
		methods=['post'],
		permission_classes=[
		AllowAny,
		],
		url_name='retrieve_up',
		url_path='action/retrieve_up',
	)
	def retrieve_up(self, request, pk=None):
		res = {}
		if request.data['action'] == 'reset_password':
			try:
				birthday = request.data['birthday'].split('-')
				birthday = [int(i) for i in birthday]
				birthday = datetime.date(birthday[0], birthday[1], birthday[2])
				user = User.objects.get(username=request.data['username'],
					birthday=birthday)
			except:
				res['message'] = u'無法取得使用者資料，請確認填寫的資料是否無誤'
				return Response(data=res,
					status=status.HTTP_406_NOT_ACCEPTABLE)
			import random
			import string
			reset_password = ''.join(
				random.choice(string.ascii_uppercase + string.digits)
				for _ in range(6))
			user.set_password(reset_password)
			subject = u'重設密碼郵件'
			message = u'您的新密碼為：{0}'.format(reset_password)
			user.email_user(subject=subject, message=message)
			user.save()
		elif request.data['action'] == 'get_user':
			try:
				birthday = request.data['birthday'].split('-')
				birthday = [int(i) for i in birthday]
				birthday = datetime.date(birthday[0], birthday[1], birthday[2])
				user = User.objects.get(email=request.data['email'],
					birthday=birthday)
			except BaseException as e:
				res['message'] = u'無法取得使用者資料，請確認填寫的資料是否無誤' + str(e)
				return Response(data=res,
					status=status.HTTP_406_NOT_ACCEPTABLE)
			subject = u'取得username郵件'
			message = u'您的username為：{0}'.format(user.username)
			user.email_user(subject=subject, message=message)

		return Response(data=res, status=status.HTTP_202_ACCEPTED)

	@action(
		detail=False,
		methods=['post'],
		url_name='email',
		url_path='action/email',
	)
	def email(self, request, pk=None):
		res = {}

		from django.core.mail import EmailMessage
		if request.data['category'] == 'editor':
			user_email_list = [
				i.email for i in User.objects.filter(is_editor=True)
				if i.is_book and i.auth_email
			]
		if request.data['category'] == 'guest':
			user_email_list = [
				i.email for i in User.objects.filter(is_guest=True)
				if i.is_book and i.auth_email
			]
		subject = request.data['subject']
		body = request.data['body']
		email = EmailMessage(subject=subject,
			body=body,
			from_email=SERVICE,
			to=[SERVICE],
			bcc=user_email_list)
		email.send(fail_silently=False)

		return Response(data=res, status=status.HTTP_202_ACCEPTED)

	@action(
		detail=True,
		methods=['get', 'post'],
		url_name='verify',
		url_path='action/verify',
	)
	def verify(self, request, pk=None):
		res = {}
		obj = self.get_object()
		if request.data['type'] == 'email' and request.data[
			'action'] == 'generate':
			if obj.email not in cache:
				import random
				import string
				vcode = ''.join(
					random.choice(string.ascii_uppercase + string.digits)
					for _ in range(6))
				cache.set(obj.email, {'vcode': vcode}, 600)
			else:
				vcode = cache.get(obj.email)['vcode']
			subject = '[驗證] {0} 信箱驗證碼'.format(obj.username)
			t = get_template('email/email_validate.txt')
			body = t.render(locals())
			email = EmailMessage(subject=subject,
				body=body,
				from_email=SERVICE,
				to=[obj.email])
			email.send(fail_silently=False)
			res['detail'] = u'已寄送到您的電子信箱'
		elif request.data['type'] == 'phone' and request.data[
			'action'] == 'generate':
			if obj.phone not in cache:
				import random
				import string
				vcode = ''.join(random.choice(string.digits) for _ in range(6))
				cache.set(request.user.phone, {'vcode': vcode}, 600)
			else:
				vcode = cache.get(request.user.phone)['vcode']
			import urllib.parse
			data = u'親愛的{0}您的信箱驗證碼為：{1}，請在10分鐘內輸入。\n'.format(
				request.user.username, vcode)
			url = 'https://api2.kotsms.com.tw/kotsmsapi-1.php?username={0}&password={1}&dstaddr={2}&smbody={3}'.format(
				OTP_ACCOUNT, OTP_PASSWORD, request.user.phone,
				urllib.parse.quote(data.encode('big5')))
			session = requests.Session()
			response = session.get(url)
			if int(response.text.split('=')[1]) > 0:
				res['detail'] = u'已寄送到您的手機'
			else:
				res['detail'] = u'請確認手機號碼是否正確或聯絡系統管理員'
				return Response(data=res,
					status=status.HTTP_406_NOT_ACCEPTABLE)
		elif request.data['type'] == 'email' and request.data[
			'action'] == 'verify':
			if obj.email not in cache:
				res['detail'] = u'驗證碼已過期，請重新產生驗證碼'
				return Response(data=res,
					status=status.HTTP_406_NOT_ACCEPTABLE)
			input_vcode = request.data['code']
			vcode = cache.get(obj.email)['vcode']
			if input_vcode == vcode:
				res['detail'] = u'信箱驗證通過'
				obj.auth_email = True
				obj.save()
			else:
				res['detail'] = u'信箱驗證碼不符'
				return Response(data=res,
					status=status.HTTP_406_NOT_ACCEPTABLE)
		elif request.data['type'] == 'phone' and request.data[
			'action'] == 'verify':
			if obj.phone not in cache:
				res['detail'] = u'驗證碼已過期，請重新產生驗證碼'
				return Response(data=res,
					status=status.HTTP_406_NOT_ACCEPTABLE)
			input_vcode = request.data['code']
			vcode = cache.get(obj.phone)['vcode']
			if input_vcode == vcode:
				res['detail'] = u'手機驗證通過'
				obj.auth_phone = True
				obj.save()
			else:
				res['detail'] = u'手機驗證碼不符'
				return Response(data=res,
					status=status.HTTP_406_NOT_ACCEPTABLE)
		return Response(data=res, status=status.HTTP_202_ACCEPTED)

	@action(
		detail=True,
		methods=['post'],
		url_name='set-password',
		url_path='action/set_password',
	)
	def set_password(self, request, pk=None):
		obj = self.get_object()
		from django.contrib.auth import authenticate, update_session_auth_hash
		user = authenticate(username=obj.username,
			password=self.request.data['oldPassword'])
		if user is not None and self.request.data[
			'newPassword1'] == self.request.data['newPassword2']:
			user.set_password(self.request.data['newPassword1'])
			user.save()
			update_session_auth_hash(request, user)
			return Response(data={'detail': u'變更密碼成功'},
				status=status.HTTP_202_ACCEPTED)
		return Response(data={'detail': u'變更密碼失敗'},
			status=status.HTTP_406_NOT_ACCEPTABLE)


class DisabilityCardViewSet(MixedPermissionModelViewSet, viewsets.ModelViewSet,
	ResourceViewSet):
	queryset = DisabilityCard.objects.all()
	serializer_class = DisabilityCardSerializer
	permission_classes_by_action = {
		'create': [AllowAny],
	}
	filter_backends = (
		filters.OrderingFilter,
		filters.SearchFilter,
		OwnerOrgManagerFilter,
		DisabilityCardActiveFilter,
		DisabilityCardOrgFilter,
	)
	search_fields = (
		'identity_card_number',
		'name',
	)

	def get_fullpath(self, obj, dir, resource):
		fullpath = None
		if dir == 'source':
			if resource == 'front':
				fullpath = obj.front
			if resource == 'back':
				fullpath = obj.back
		return fullpath


class ServiceInfoViewSet(viewsets.ModelViewSet, ResourceViewSet):
	queryset = ServiceInfo.objects.all().order_by('-date')
	serializer_class = ServiceInfoSerializer
	filter_backends = (
		filters.OrderingFilter,
		OwnerOrgManagerFilter,
		OwnerFilter,
		OrgFilter,
		ServiceInfoExchangeFilter,
	)
	ordering_fields = ('owner', )
	permission_classes = (permissions.IsAuthenticated, )

	def perform_create(self, serializer):
		instance = serializer.save()
		instance.service_hours = instance.get_service_hours()
		instance.save()

	@action(
		detail=False,
		methods=['get'],
		url_name='exchange_false_export',
		url_path='action/exchange_false_export',
	)
	def exchange_false_export(self, request, pk=None):
		path = ServiceInfo.exchange_false_export()
		return self.get_resource(path)


class AnnouncementViewSet(viewsets.ModelViewSet, ResourceViewSet):
	queryset = Announcement.objects.all().order_by('-datetime')
	serializer_class = AnnouncementSerializer
	filter_backends = (
		filters.OrderingFilter,
		filters.SearchFilter,
		dffilters.DjangoFilterBackend,
	)
	ordering_fields = ('datetime', )
	search_fields = ('category', )
	filterset_fields = ('category', 'org_id')
	permission_classes = (RuleORPermissionFactory('list', [
		'is_manager',
		'__read__',
	]), )

	def get_fullpath(self, obj, dir, resource):
		fullpath = os.path.join(obj.path, dir, resource)
		return fullpath

	@action(
		detail=False,
		methods=['get'],
		url_name='latest',
		url_path='action/latest',
	)
	def latest(self, request, pk=None):
		from datetime import datetime
		from dateutil.relativedelta import relativedelta
		year = datetime.today().year
		month = datetime.today().month
		begin_date = datetime(year, month, 1) + relativedelta(months=-12)
		end_date = datetime.today()

		query = Announcement.objects

		category = request.query_params.get('category')
		if category:
			query = query.filter(category=category)
		query = query.filter(datetime__gte=begin_date, datetime__lte=end_date).order_by("-datetime")
		s = AnnouncementSerializer(instance=query, many=True)
		return Response(data=s.data, status=status.HTTP_202_ACCEPTED)

class QAndAViewSet(viewsets.ModelViewSet):
	queryset = QAndA.objects.all()
	serializer_class = QAndASerializer
	filter_backends = (QAndACategoryFilter, )
	permission_classes = (RuleORPermissionFactory('list', [
		'is_manager',
		'__read__',
	]), )

	def perform_create(self, serializer):
		instance = serializer.save(order=len(QAndA.objects.all()), )
		instance.save()


class OrganizationViewSet(viewsets.ModelViewSet):
	queryset = Organization.objects.all()
	serializer_class = OrganizationSerializer
	filter_backends = (
		filters.OrderingFilter,
		filters.SearchFilter,
	)
	permission_classes = (RuleORPermissionFactory('list', [
		'is_manager',
		'__read__',
	]), )


class BusinessContentViewSet(viewsets.ModelViewSet):
	queryset = BusinessContent.objects.all()
	serializer_class = BusinessContentSerializer
	permission_classes = (RuleORPermissionFactory('list', [
		'is_manager',
		'__read__',
	]), )


class BannerContentViewSet(viewsets.ModelViewSet, ResourceViewSet):
	queryset = BannerContent.objects.all()
	serializer_class = BannerContentSerializer
	filter_backends = (dffilters.DjangoFilterBackend, )
	filterset_fields = ('category', )
	permission_classes = (RuleORPermissionFactory('list', [
		'is_manager',
		'__read__',
	]), )
	"""def perform_create(self, serializer):
		instance = serializer.save(
			order = len(BannerContent.objects.all()),
		)
		instance.save()"""
	def get_fullpath(self, obj, dir, resource):
		fullpath = None
		if dir == 'cover':
			if resource == 'image':
				fullpath = obj.cover_image
		return fullpath


class RecommendationSubjectViewSet(viewsets.ModelViewSet, ResourceViewSet):
	queryset = RecommendationSubject.objects.all()
	serializer_class = RecommendationSubjectSerializer
	filter_backends = (dffilters.DjangoFilterBackend, )
	permission_classes = (RuleORPermissionFactory('list', [
		'is_manager',
		'__read__',
	]), )

	def perform_create(self, serializer):
		instance = serializer.save(order=len(
			RecommendationSubject.objects.all()), )
		instance.save()

	def get_fullpath(self, obj, dir, resource):
		fullpath = None
		if dir == 'cover':
			if resource == 'image':
				fullpath = obj.cover_image
		return fullpath
