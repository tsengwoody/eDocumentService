# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest


class NewMaterialContentTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.browser.maximize_window()

    def tearDown(self):
        self.browser.quit()

    def testCreateNewMaterial(self):
        self.browser.get('http://192.168.1.70/auth/register/')
        radio = self.browser.find_element_by_id('id_editor')
        print radio

if __name__ == '__main__':
    unittest.main()