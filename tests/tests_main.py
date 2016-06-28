#*********************************************************************
# File: tests/__init__.py
# Description: A skeleton for Sandbox unittests
# To run type this command: python run.py test
#*********************************************************************
import unittest
from flask import current_app, url_for
from app import create_app
from selenium import webdriver

class BasicsTestCase(unittest.TestCase):
	def setUp(self):
		self.app = create_app('testing')
		self.app_context = self.app.app_context()
		self.app_context.push()
		self.client = self.app.test_client(use_cookies=True)
		self.driver = None
		
	def tearDown(self):		
		self.app_context.pop()
		if self.driver is not None:
			self.driver.close()

	def test_app_exists(self):
		self.assertFalse(current_app is None)

	def test_app_is_testing(self):		
		self.assertTrue(current_app.config['TESTING'])
		self.assertEqual(current_app.config['BASEURL'], 'http:/www.ci.workopolis.com')		

	def test_home_page(self):
		response = self.client.get(url_for('common.main'))		
		self.assertTrue('Workopolis Job Search POC' in response.get_data(as_text=True))

	def test_search_button(self):				
		self.driver = webdriver.Firefox()
		self.driver.get(current_app.config['BASEURL'])		
		find_button = self.driver.find_element_by_id('btn-jobsearch-find-jobs')		
		assert "Workopolis" in self.driver.title
				

		
