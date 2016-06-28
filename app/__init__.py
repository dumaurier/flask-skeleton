#******************************************************************
# File: app/__init__.py
# Description: This is the application factory that allows 
# configuring the app before running it. Registers Blueprints,
# initializes Babel for translations and resource file revisioning. :) :)
#******************************************************************

from flask import Flask, Blueprint, render_template, request, g, redirect
from jinja2 import Markup
from flask.ext.babel import Babel
from config import CONFIG, LANGUAGES
from .context_processor import revved_url_for, init_revisioned_urls
from .blueprintsample import blueprintsample as blueprintsample

babel = Babel()

def create_app(config_name):
	app = Flask(__name__)	

	# Apply configurations
	app.config.from_object(CONFIG[config_name])

	# Allow including raw templates without being escaped (e.g. Hogan templates)
	app.jinja_env.globals['include_raw'] = lambda filename : Markup(app.jinja_loader.get_source(app.jinja_env, filename)[0])

	# Check for versioning of static assets
	app.context_processor(revved_url_for)
	init_revisioned_urls(app)

	# Register blueprints and init routes
	register_app_blueprints(app)
	init_app_routes(app)

	# Bind the translations
	babel.init_app(app)
	@babel.localeselector
	def get_locale():
		if 'language' in g:			
			return g.language
		return request.accept_languages.best_match(['fr', 'en'])

	return app


# ****************** DEFINE APP HELPER METHODS *************************

# Register all bluprints
def register_app_blueprints(app):
	app.register_blueprint(blueprintsample)


# Define a handler for binding post-request callback functions
def bind_request_callbacks(f):
	if not hasattr(g, 'after_request_callbacks'):
		g.after_request_callbacks = []
	g.after_request_callbacks.append(f)
	return f


# Define custom error pages that belong to the app, not blueprints
def init_app_routes(app):

	# "Page not found" handler
	@app.errorhandler(404)
	def page_not_found(e):
		return render_template('404.html'), 404

	# "Server error" handler
	@app.errorhandler(500)
	def internal_server_error(e):
		return render_template('500.html'), 500

	# Language cookie settings before the request
	@app.before_request
	def detect_user_language():
		language = request.cookies.get('WorkLang')
		if language is None:
			language = g.language if 'language' in g else request.accept_languages.best_match(['fr', 'fr-CA', 'en', 'en-CA'])
			if language == 'fr-CA':
				g.language = 'fr'
			elif language == 'en-CA':
				g.language = 'en'
			else:
				g.language = language
			# The post-request Cookie setter (callback)
			@bind_request_callbacks
			def remember_language(response):
				response.set_cookie('WorkLang', g.language, max_age=1209600) #14 days
		else:
			g.language = language

	# temporary fix upon site load, blueprint root not being respected
	@app.route('/')
	def index():
		return redirect("/"+g.language, code=302)


	# Invoke all post-request callback methods
	@app.after_request
	def call_after_request_callbacks(response):
		for callback in getattr(g, 'after_request_callbacks', ()):
			callback(response)
		return response



