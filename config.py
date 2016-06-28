# -*- coding: utf-8 -*-
import os

class Config:
	BASEURL = 'http:/www.workopolis.com'
	LOG_LEVEL = 'ERROR'

class DevelopmentConfig(Config):
	DEBUG = True
	BASEURL = 'http:/localhost'
	LOG_LEVEL = 'DEBUG'

class TestingConfig(Config):
	TESTING = True
	BASEURL = 'http:/www.ci.workopolis.com'
	LOG_LEVEL = 'INFO'

class ProductionConfig(Config):	
	BASEURL = 'http:/www.workopolis.com'

CONFIG = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'default': DevelopmentConfig
}

# available languages
LANGUAGES = {
    'primary': {'lang-code': 'en', 'lang-name': 'English'},
    'secondary': {'lang-code': 'fr', 'lang-name': 'Français'},
    'default': {'lang-code': 'en', 'lang-name': 'English'}
}