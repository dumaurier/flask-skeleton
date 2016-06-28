#*********************************************************************
# File: blueprintsample/__init__.py
# Description: This is the Blueprint for Common.
# All Common routes are defined here to render appropriate templates.
#*********************************************************************

import requests
import json
from flask import Flask, Blueprint, render_template, g
from config import LANGUAGES

# Define Blueprints and the global var blueprintsample
blueprintsample = Blueprint('blueprintsample', __name__ ,url_prefix='/<lang_code>')

@blueprintsample.url_defaults
def add_lang_code(endpoint, values):
	values.setdefault('lang_code', g.language)

@blueprintsample.url_value_preprocessor
def pull_lang_code(endpoint, values):
	g.language = values.pop('lang_code')

@blueprintsample.route('/')
def main():
	return render_template('index.html')

