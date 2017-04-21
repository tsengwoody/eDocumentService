# coding: utf-8
import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time

MAX_WAIT = 10

from django.core.urlresolvers import reverse, resolve
from selenium.webdriver.common.action_chains import ActionChains
from account.models import *
from ebookSystem.models import *
from genericUser.models import *
from guest.models import *

class FunctionalTest(StaticLiveServerTestCase):

	def setUp(self):
		root = User(username='root', email='edocumentservice@gmail.com', first_name = 'demo root firstname', last_name = 'demo root lastname', is_active=True, is_superuser=True, is_staff=True, phone='0917823099', birthday='2016-01-01', is_editor=True, is_guest=True, is_manager=True, is_advanced_editor=True, education=u'學士')
		root.set_password('root')
		root.status = root.STATUS['active']
		root.auth_email = True
		root.auth_phone = True
		root.auth_privacy = True
		root.save()
		rootEditor = Editor.objects.create(user=root, professional_field=u'資訊工程學')
		rootGuest = Guest.objects.create(user=root)
		self.browser = webdriver.Firefox()

	def test_login(self):

		self.browser.get(self.live_server_url +reverse('login'))
		element = self.browser.find_element_by_id("id_username")
		element.send_keys("root")
		element = self.browser.find_element_by_id("id_password")
		element.send_keys("root")
		self.browser.find_element_by_id("id_submit").click()
		self.wait_for(lambda: self.assertIn(
			"Success",
			self.browser.find_element_by_id('successDialog').text
		))
		successDialog = self.browser.find_element_by_id('successDialog')
		successDialog.click()

		self.browser.get(self.live_server_url +reverse('login'))
		element = self.browser.find_element_by_id("id_username")
		element.send_keys("root")
		element = self.browser.find_element_by_id("id_password")
		element.send_keys("root")
		self.browser.find_element_by_id("id_submit").click()
		self.wait_for(lambda: self.assertIn(
			"Success",
			self.browser.find_element_by_id('successDialog').text
		))
		successDialog = self.browser.find_element_by_id('successDialog')
		successDialog.click()
		self.assertIn('/genericUser/license', self.browser.current_url)

	def test_upload(self):
		print self.browser.current_url

	def tearDown(self):
		self.browser.quit()


	def wait_for(self, fn):
		start_time = time.time()
		while True:
			try:
				return fn()
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)
