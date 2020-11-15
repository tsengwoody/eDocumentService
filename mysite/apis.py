# coding: utf-8

#import datetime
import os

import pandas as pd

from django.db.models import Count, Sum
from django.utils import timezone as datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from ebookSystem.models import *
from genericUser.models import *

from utils.resource import Resource

class Statistics(APIView):
	begin_time = None
	end_time = None

	def filter_time(self, request):

		import pytz
		utc = pytz.timezone('UTC')

		begin_time = request.query_params.get('begin_time')
		if begin_time:
			temp_time = begin_time.split('-')
			temp_time = [int(i) for i in temp_time]
			self.begin_time = datetime.datetime(temp_time[0], temp_time[1], temp_time[2], tzinfo=utc)

		end_time = request.query_params.get('end_time')
		if end_time:
			temp_time = end_time.split('-')
			temp_time = [int(i) for i in temp_time]
			self.end_time = datetime.datetime(temp_time[0], temp_time[1], temp_time[2], tzinfo=utc)

	def filter_org(self, request):

		org_id = request.GET.get('org_id', None)
		if org_id:
			try:
				self.org = Organization.objects.get(id=org_id)
			except:
				self.org = None

	def get(self, request, action=None):
		res = {}
		self.filter_time(request)
		self.filter_org(request)

		if action:
			#try:
			return getattr(self, action)(request)
			#except BaseException as e:
				#return Response(data=res, status=status.HTTP_406_NOT_ACCEPTABLE)

	def summary(request, template_name='mysite/statistics.html'):
		from utils.other import month_gen
		from ebookSystem.models import Book
		from genericUser.models import User

		month_list = month_gen(count=6)
		month_list.insert(0, datetime.datetime.today())
		result = []
		for month in month_list:
			editor_count = User.objects.filter(is_editor=True, date_joined__lte=month, auth_email=True, auth_phone=True,).count()
			guest_count = User.objects.filter(is_guest=True, date_joined__lte=month, auth_email=True, auth_phone=True,).count()
			editor_count_30 = User.objects.filter(is_editor=True, date_joined__lte=month, online__gt=month -datetime.timedelta(days=30), auth_email=True, auth_phone=True,).count()
			finish_count = Book.objects.filter(finish_date__lte=month, upload_date__lte=month, source='self').count()
			txt_count = Book.objects.filter(upload_date__lte=month, source='txt').count()
			epub_count = Book.objects.filter(upload_date__lte=month, source='epub').count()
			book_count = Book.objects.filter(upload_date__lte=month).count()
			scanbook_count = Book.objects.filter(upload_date__lte=month, source='self').count()
			result.append({
				'month': month,
				'editor_count': editor_count,
				'guest_count': guest_count,
				'editor_count_30': editor_count_30,
				'book_count': book_count,
				'scanbook_count': scanbook_count,
				'finish_count': finish_count,
				'txt_count': txt_count,
				'epub_count': epub_count,
			})
		return Response(data=result, status=status.HTTP_202_ACCEPTED)

	def book_download(self, request):
		res = {}
		res['result'] = []

		query = GetBookRecord.objects.all()
		if self.begin_time:
			query = query.filter(get_time__gte=self.begin_time)
		if self.end_time:
			query = query.filter(get_time__lt=self.end_time)
		if hasattr(self, 'org'):
			query = query.filter(user__org=self.org)

		file_format = request.GET.get('file_format', None)
		if file_format:
			query = query.filter(format=file_format)

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
		if hasattr(self, 'org'):
			query = query.filter(user__org=self.org)
		download_count = query.count()

		res['result'].append({
			'groupfield': 'all',
			'count': download_count,
		})
		r = query.values('user').annotate(count=Count('user'))
		r = [{
			'groupfield': User.objects.get(id=i['user']).first_name +User.objects.get(id=i['user']).last_name,
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
		if hasattr(self, 'org'):
			query = query.filter(editor__org=self.org)
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

	def book_download_pd(self, request):
		from django.db.models.functions import TruncMonth
		from django.db.models import Count

		res = {}

		query = GetBookRecord.objects.all()
		if self.begin_time:
			query = query.filter(get_time__gte=self.begin_time)
		if self.end_time:
			query = query.filter(get_time__lt=self.end_time)
		if hasattr(self, 'org'):
			query = query.filter(user__org=self.org)

		file_format = request.GET.get('file_format', None)
		if file_format:
			query = query.filter(format=file_format)

		groupby = query.annotate(month=TruncMonth('get_time')).values('month', 'book').annotate(count=Count('id'))
		df = pd.DataFrame(groupby)
		if df.empty:
			res['result'] = list()
			return Response(data=res, status=status.HTTP_202_ACCEPTED)
		df['month'] = df['month'].apply(lambda x: str(x)[0:10])
		df_month = df.pivot(index='book', columns='month', values='count').reset_index()
		groupby = query.values('book').annotate(count=Count('id'))
		df_all = pd.DataFrame(groupby)
		df = pd.merge(df_all, df_month, how='outer', left_on='book', right_on='book').fillna(0)
		df_sum = df.sum()
		df_sum['book'] = -1
		df = df.append(df_sum, ignore_index=True)

		books = BookInfo.objects.all().values('ISBN', 'bookname')
		df_book = pd.DataFrame(books)
		s = pd.Series({'ISBN': '-1', 'bookname': '全部'})
		df_book = df_book.append(s, ignore_index=True)
		df = pd.merge(df, df_book, how='left', left_on='book', right_on='ISBN').fillna('').drop('ISBN', axis=1)
		df = df.rename(columns={'bookname': 'index', 'count': 'all', 'book': 'id'})

		dicts = df.to_dict(orient='index')
		res['result'] = list(dicts.values())
		return Response(data=res, status=status.HTTP_202_ACCEPTED)

	def user_download_pd(self, request):
		from django.db.models.functions import TruncMonth
		from django.db.models import Count

		res = {}

		query = GetBookRecord.objects.all()
		if self.begin_time:
			query = query.filter(get_time__gte=self.begin_time)
		if self.end_time:
			query = query.filter(get_time__lt=self.end_time)
		if hasattr(self, 'org'):
			query = query.filter(user__org=self.org)

		groupby = query.annotate(month=TruncMonth('get_time')).values('month', 'user').annotate(count=Count('id'))
		df = pd.DataFrame(groupby)
		if df.empty:
			res['result'] = list()
			return Response(data=res, status=status.HTTP_202_ACCEPTED)
		df['month'] = df['month'].apply(lambda x: str(x)[0:10])
		df_month = df.pivot(index='user', columns='month', values='count').reset_index()
		groupby = query.values('user').annotate(count=Count('id'))
		df_all = pd.DataFrame(groupby)
		df = pd.merge(df_all, df_month, how='outer', left_on='user', right_on='user').fillna(0)
		df_sum = df.sum()
		df_sum['user'] = -1
		df = df.append(df_sum, ignore_index=True)

		from genericUser.models import User
		users = User.objects.all().values('id', 'username')
		df_user = pd.DataFrame(users)
		s = pd.Series({'id': -1, 'username': '全部'})
		df_user = df_user.append(s, ignore_index=True)
		df = pd.merge(df, df_user, how='left', left_on='user', right_on='id').fillna('').drop('id', axis=1)
		df = df.rename(columns={'username': 'index', 'count': 'all', 'user': 'id'})

		dicts = df.to_dict(orient='index')
		res['result'] = list(dicts.values())
		return Response(data=res, status=status.HTTP_202_ACCEPTED)

	def user_editrecord_pd(self, request):
		from django.db.models.functions import TruncMonth
		from django.db.models import Count

		res = {}

		query = EditRecord.objects.all()
		if self.begin_time:
			query = query.filter(get_date__gte=self.begin_time)
		if self.end_time:
			query = query.filter(get_date__lt=self.end_time)
		if hasattr(self, 'org'):
			query = query.filter(editor__org=self.org)
		groupby = query.annotate(month=TruncMonth('get_date')).values('month', 'editor').annotate(count=Count('id'))
		df = pd.DataFrame(groupby)
		if df.empty:
			res['result'] = list()
			return Response(data=res, status=status.HTTP_202_ACCEPTED)
		df['month'] = df['month'].apply(lambda x: str(x))
		df_month = df.pivot(index='editor', columns='month', values='count').reset_index()
		groupby = query.values('editor').annotate(count=Count('id'))
		df_all = pd.DataFrame(groupby)
		df = pd.merge(df_all, df_month, how='outer', left_on='editor', right_on='editor').fillna(0)
		df_sum = df.sum()
		df_sum['editor'] = -1
		df = df.append(df_sum, ignore_index=True)

		from genericUser.models import User
		users = User.objects.all().values('id', 'username')
		df_user = pd.DataFrame(users)
		s = pd.Series({'id': -1, 'username': '全部'})
		df_user = df_user.append(s, ignore_index=True)
		df = pd.merge(df, df_user, how='left', left_on='editor', right_on='id').fillna('').drop('id', axis=1)
		df = df.rename(columns={'username': 'index', 'count': 'all', 'editor': 'id'})

		dicts = df.to_dict(orient='index')
		res['result'] = list(dicts.values())
		return Response(data=res, status=status.HTTP_202_ACCEPTED)

	def serviceinfo(self, request):
		res = []
		query = EditRecord.objects.all()
		if self.begin_time:
			query = query.filter(get_date__gte=self.begin_time)
		if self.end_time:
			query = query.filter(get_date__lt=self.end_time)
		if hasattr(self, 'org'):
			query = query.filter(editor__org=self.org)

		r = query.values('editor').annotate(count=Sum('service_hours'))
		r = [{
			'username': unicode(User.objects.get(id=i['editor'])),
			'email': User.objects.get(id=i['editor']).email,
			'phone': User.objects.get(id=i['editor']).phone,
			'count': i['count'],
		} for i in r if i['editor']]
		res.extend(r)

		return Response(data=res, status=status.HTTP_202_ACCEPTED)

	def user_read(self, request):
		res = []

		# 借閱的資料
		query = LibraryRecord.objects.all()
		if self.begin_time:
			query = query.filter(check_out_time__gte=self.begin_time)
		if self.end_time:
			query = query.filter(check_out_time__lt=self.end_time)
		if hasattr(self, 'org'):
			query = query.filter(owner__org=self.org)

		library_result = query.values('owner').annotate(count=Count('owner'))
		library_result = [{
			'user': i['owner'],
			'library': i['count'],
		} for i in library_result if i['owner']]

		# 下載的資料
		query = GetBookRecord.objects.all()
		if self.begin_time:
			query = query.filter(get_time__gte=self.begin_time)
		if self.end_time:
			query = query.filter(get_time__lt=self.end_time)
		if hasattr(self, 'org'):
			query = query.filter(user__org=self.org)

		download_result = query.values('user').annotate(count=Count('user'))
		download_result = [{
			'user': i['user'],
			'download': i['count'],
		} for i in download_result if i['user']]

		df1 = pd.DataFrame(library_result)
		df2 = pd.DataFrame(download_result)
		df = df1.set_index('user').join(df2.set_index('user'), how='outer')
		df = df.fillna(0)
		datas = df.reset_index().to_dict(orient='record')
		for i in datas:
			u = User.objects.get(id=i['user'])
			res.append({
				'user': unicode(u),
				'join': u.date_joined,
				'library': i['library'],
				'download': i['download'],
			})

		return Response(data=res, status=status.HTTP_202_ACCEPTED)

	def book_read(self, request):
		res = []

		# 借閱的資料
		query = LibraryRecord.objects.all()
		if self.begin_time:
			query = query.filter(check_out_time__gte=self.begin_time)
		if self.end_time:
			query = query.filter(check_out_time__lt=self.end_time)
		if hasattr(self, 'org'):
			query = query.filter(owner__org=self.org)

		library_result = query.values('object').annotate(count=Count('object'))
		library_result = [{
			'book': i['object'],
			'library': i['count'],
		} for i in library_result if i['object']]

		# 下載的資料
		query = GetBookRecord.objects.all()
		if self.begin_time:
			query = query.filter(get_time__gte=self.begin_time)
		if self.end_time:
			query = query.filter(get_time__lt=self.end_time)
		if hasattr(self, 'org'):
			query = query.filter(user__org=self.org)

		download_result = query.values('book').annotate(count=Count('book'))
		download_result = [{
			'book': i['book'],
			'download': i['count'],
		} for i in download_result if i['book']]

		df1 = pd.DataFrame(library_result)
		df2 = pd.DataFrame(download_result)
		df = df1.set_index('book').join(df2.set_index('book'), how='outer')
		df = df.fillna(0)
		datas = df.reset_index().to_dict(orient='record')
		for i in datas:
			b = Book.objects.get(ISBN=i['book'])
			res.append({
				'bookname': b.book_info.bookname,
				'author': b.book_info.author,
				'house': b.book_info.house,
				'date': b.book_info.date,
				'upload_date': b.upload_date,
				'library': i['library'],
				'download': i['download'],
			})

		return Response(data=res, status=status.HTTP_202_ACCEPTED)

class Ddm(Resource):

	def get(self, request, action=None, *args, **kwargs):
		res = {}
		if action:
			if action == 'resource' and 'resource' in kwargs:
				return self.resource(request, kwargs['dir'], kwargs['resource'])
			elif action == 'resource' and not ('resource' in kwargs):
				return self.category(request, kwargs['dir'])
			else:
				return getattr(self, action)(request)

	def post(self, request, action=None, *args, **kwargs):
		res = {}
		if action:
			if action == 'resource' and 'resource' in kwargs:
				return self.resource(request, kwargs['dir'], kwargs['resource'])
			elif action == 'resource' and not ('resource' in kwargs):
				return self.category(request, kwargs['dir'])
			else:
				return getattr(self, action)(request)

	def delete(self, request, action=None, *args, **kwargs):
		res = {}
		if action:
			if action == 'resource' and 'resource' in kwargs:
				return self.resource(request, kwargs['dir'], kwargs['resource'])
			elif action == 'resource' and not ('resource' in kwargs):
				return self.category(request, kwargs['dir'])
			else:
				return getattr(self, action)(request)

	def resource(self, request, dir=None, resource=None):
		fullpath = os.path.join(BASE_DIR, 'file' ,'ddm', dir, resource)
		if request.method == 'GET':
			return self.get_resource(fullpath)
		if request.method == 'POST':
			return self.post_resource(fullpath, request.FILES['object'])
		if request.method == 'DELETE':
			return self.delete_resource(fullpath)

	def category(self, request, dir=None):
		fullpath = os.path.join(BASE_DIR, 'file' ,'ddm', dir)
		return self.get_resource_list(fullpath)
