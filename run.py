# Configures and runs the app
import os
from app import create_app
from flask import request
from flask.ext.script import Manager


# Create the app
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# Wrap the app within the Manager object (allows running command-line tasks) and run it
manager = Manager(app)

# This command runs the unittests. In command-line, type: python run.py test
@manager.command
def test():
	"""Run the unit tests."""
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(tests)

# Run the application
if __name__ == '__main__':
	manager.run()
