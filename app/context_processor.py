#**************************************************************
# File: context_processor.py
# Description: This module contains methods for revisioning of
# static files to bust the cache when deployed to production.
#**************************************************************

from os import path
import json
from flask import url_for, current_app, g
import ast

def revved_url_for():
    return {
        'url_for': _revved_url_for,
        'lurl_for': lambda ep, **values: url_for(ep+'_'+g.language, **values)
    }

def _revved_url_for(endpoint, **values):
    if endpoint == 'static':
        original_filename = values.get('filename')
        if original_filename:
            revved_filename = current_app.config['FILEREVS'].get(original_filename)
            if revved_filename:
                del values['filename']
                return url_for(endpoint, filename=revved_filename, **values)
    return url_for(endpoint, **values)

def init_revisioned_urls(app):
    filerevs_path = path.join('static', 'rev-manifest.json')
    try:
        with app.open_resource(filerevs_path) as filerevs_fh:
            filerevs = filerevs_fh.read().decode('utf-8')
            obj = json.loads(filerevs)
            app.config['FILEREVS'] = ast.literal_eval(filerevs)
    except IOError:
        print('No filerevs found, continuing without')
        app.config['FILEREVS'] = {}
