# coding: utf-8
from django.test import TestCase
# Create your tests here.

from django.core.urlresolvers import reverse

from account.models import Editor
from ebookSystem.models import *
from guest.models import Guest
from genericUser.models import *

class baseViewTests(TestCase):
	def setUp(self):
		p = ['active', 'editor', 'guest', 'manager', 'advanced_editor', 'root', 'license', ]
		for item in p:
			exec("permission_{0} = Permission.objects.create(name='{0}', codename='{0}')".format(item))
		root = User(username='root', email='edocumentservice@gmail.com', first_name = 'demo root firstname', last_name = 'demo root lastname', is_active=True, is_superuser=True, is_staff=True, phone='0917823099', birthday='2016-01-01', is_editor=True, is_guest=True, is_manager=True, is_advanced_editor=True, education=u'學士')
		root.set_password('root')
		root.status = root.STATUS['active']
		root.auth_email = True
		root.auth_phone = True
		root.auth_privacy = True
		root.save()
		org = Organization.objects.create(name=u'eDocumentService', address=u'台北市大同區1段149號7樓', email=u'edocumentservice@gmail.com', phone='0917823098', manager=root, is_service_center=True)
		root.org=org
		root.save()
		p = ['editor', 'guest', 'manager', 'advanced_editor', 'root', ]
		for item in p:
			exec("root.permission.add(permission_{0})".format(item))
		rootEditor = Editor.objects.create(user=root, professional_field=u'資訊工程學')
		rootGuest = Guest.objects.create(user=root)
		self.client.login(username='root', password='root')

class licenseViewTests(baseViewTests):
	def test_correct_case(self):
		response = self.client.post(
			reverse(
				'genericUser:license'
			),
			{
				u'is_privacy': u'agree',
			}
		)
		root = User.objects.get(username='root')
		self.assertTrue(Permission.objects.get(codename='license') in root.permission.all())

	def test_error_case(self):
		response = self.client.post(
			reverse(
				'genericUser:license'
			),
			{
			}
		)
		root = User.objects.get(username='root')
		self.assertTrue(Permission.objects.get(codename='license') in root.permission.all())

	def test_error_case(self):
		response = self.client.post(
			reverse(
				'genericUser:license'
			),
			{}
		)
		root = User.objects.get(username='root')
		self.assertFalse(Permission.objects.get(codename='license') in root.permission.all())

class review_user(baseViewTests):
	def test_correct_Text_case(self):
		response = self.client.post(
			reverse(
				'genericUser:review_user',
				kwargs = {
					'username': 'root',
				}
			),
			{
				'active': 'on',
				'editor': 'on',
#				'guest': 'on',
				'review': 'success',
				'reason': '',
			}
		)
		root = User.objects.get(username='root')
		for item in ['active', 'editor', ]:
			self.assertTrue(Permission.objects.get(codename=item) in root.permission.all())

class create_documentViewTests(baseViewTests):
	def test_correct_case(self):
		book_file = open(BASE_DIR +'/temp/9789866031632.zip')
		response = self.client.post(
			reverse(
				'genericUser:create_document'
			),
{
				u'ISBN': u'9789866031632',
				u'author': u'湯姆.狄馬克(Tom DeMarco), 提摩西.李斯特(Timothy Lister)著; 錢一一譯',
				u'house': u'經濟新潮社',
				u'bookname': u'Peopleware腦力密集產業的人才管理之道',
				u'date': u'2014-12-01',
				u'bookbinding': '平裝',
				u'chinese_book_category': '494',
				u'order': '二版',
				'fileObject': book_file,
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		book_file.close()
		print response.json()['message']
		self.assertEqual(len(Book.objects.all()), 1, len(Book.objects.all()))

	def tearDown(self):
		try:
			shutil.rmtree(BASE_DIR +'/file/ebookSystem/document/{}'.format('9789866031632'))
#			shutil.rmtree(os.path.join(BASE_DIR, '/file/ebookSystem/document/9789866031632'))
		except BaseException as e:
			print('error')
			print(e)

class upload_documentViewTests(baseViewTests):
	def test_correct_epub_case(self):
		book_file = open(BASE_DIR +u'/temp/自創思維.epub')
		response = self.client.post(
			reverse(
				'genericUser:upload_document'
			),
			{
				u'ISBN': u'9789863981454',
				u'author': u'雷德.霍夫曼(Reid Hoffman), 班.卡斯諾查(Ben Casnocha)著; 洪慧芳譯',
				u'house': u'天下雜誌',
				u'bookname': u'自創思維: 人生是永遠的測試版,瞬息萬變世界的新工作態度',
				u'date': u'2016-02-01',
				u'bookbinding': '平裝',
				u'chinese_book_category': '494',
				u'order': '第二版',
				'fileObject': book_file,
				'category': 'epub',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		book_file.close()
		print response.json()['message']
		self.assertEqual(len(Book.objects.all()), 1, len(Book.objects.all()))
		book = Book.objects.first()
		shutil.rmtree(book.path)

	def test_correct_txt_case(self):
		book_file = open(BASE_DIR +u'/temp/9789862621684.txt')
		response = self.client.post(
			reverse(
				'genericUser:upload_document'
			),
			{
				u'ISBN': u'9789862621684',
				u'author': u'朝井遼著; 黃薇嬪譯',
				u'house': u'貓頭鷹',
				u'bookname': u'聽說桐島退社了',
				u'date': u'2013-09-01',
				u'bookbinding': '平裝',
				u'chinese_book_category': '861',
				u'order': '初版',
				'fileObject': book_file,
				'category': 'txt',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		book_file.close()
		print response.json()['message']
		self.assertEqual(len(Book.objects.all()), 1, len(Book.objects.all()))
		book = Book.objects.first()
		shutil.rmtree(book.path)

	def tearDown(self):
		try:
			pass
		except BaseException as e:
			print(e)
