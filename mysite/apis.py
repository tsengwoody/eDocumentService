# coding: utf-8

import datetime

from django.db.models import Count

from rest_framework.decorators import list_route, detail_route
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from ebookSystem.models import *
from genericUser.models import *

class Statistics(APIView):
	begin_time = None
	end_time = None

	def filter_time(self, request):

		begin_time = request.GET.get('begin_time', None)
		if begin_time:
			temp_time = begin_time.split('-')
			temp_time = [int(i) for i in temp_time]
			self.begin_time = datetime.datetime(temp_time[0], temp_time[1], temp_time[2])

		end_time = request.GET.get('end_time', None)
		if end_time:
			temp_time = end_time.split('-')
			temp_time = [int(i) for i in temp_time]
			self.end_time = datetime.datetime(temp_time[0], temp_time[1], temp_time[2])

	def get(self, request, action=None):
		res = {}
		self.filter_time(request)
		if action:
			#try:
			return getattr(self, action)(request)
			#except BaseException as e:
				#return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)

	def download(self, request):
		res = {}

		query = GetBookRecord.objects.all()
		if self.begin_time:
			query = query.filter(get_time__gte=self.begin_time)
		if self.end_time:
			query = query.filter(get_time__lt=self.end_time)
		download_count = query.count()

		res['download_count'] = download_count
		return Response(data=res, status=status.HTTP_202_ACCEPTED)

	def book_download(self, request):
		res = {}
		res['result'] = []

		query = GetBookRecord.objects.all()
		if self.begin_time:
			query = query.filter(get_time__gte=self.begin_time)
		if self.end_time:
			query = query.filter(get_time__lt=self.end_time)
		download_count = query.count()

		res['result'].append({
			'groupfield': 'all',
			'count': download_count,
		})
		r = query.values('book').annotate(count=Count('book')) 
		r = [{
			'groupfield': BookInfo.objects.get(ISBN=i['book']).bookname,
			'count': i['count'],
		} for i in r if i['book']]
		res['result'].extend(r)

		return Response(data=res, status=status.HTTP_202_ACCEPTED)

	def user_download(self, request):
		res = {}
		res['result'] = []

		query = GetBookRecord.objects.all()
		if self.begin_time:
			query = query.filter(get_time__gte=self.begin_time)
		if self.end_time:
			query = query.filter(get_time__lt=self.end_time)
		download_count = query.count()

		res['result'].append({
			'groupfield': 'all',
			'count': download_count,
		})
		r = query.values('user').annotate(count=Count('user'))
		r = [{
			'groupfield': User.objects.get(id=i['user']).username,
			'count': i['count'],
		} for i in r if i['user']]
		res['result'].extend(r)

		return Response(data=res, status=status.HTTP_202_ACCEPTED)

	def user_editrecord(self, request):
		res = {}
		res['result'] = []

		query = EditRecord.objects.all()
		if self.begin_time:
			query = query.filter(get_date__gte=self.begin_time)
		if self.end_time:
			query = query.filter(get_date__lt=self.end_time)
		count = query.count()

		res['result'].append({
			'groupfield': 'all',
			'count': count,
		})
		r = query.values('editor').annotate(count=Count('editor'))
		r = [{
			'groupfield': User.objects.get(id=i['editor']).username,
			'count': i['count'],
		} for i in r if i['editor'] ]
		res['result'].extend(r)

		return Response(data=res, status=status.HTTP_202_ACCEPTED)

		#end_time = datetime.datetime.now()
		#begin_time = datetime.datetime.now() +datetime.timedelta(days=-200)