from flaskr import pages, login
from flaskr.backend import Backend # import our Backend implementation
from flask_login import LoginManager
from flask import Flask

import logging
logging.basicConfig(level=logging.DEBUG)

# The flask terminal command inside "run-flask.sh" searches for
# this method inside of __init__.py (containing flaskr module 
# properties) as we set "FLASK_APP=flaskr" before running "flask".
def create_app(test_config=None):
    # Create and configure the app.
    app = Flask(__name__, instance_relative_config=True)

    # This is the default secret key used for login sessions
    # By default the dev environment uses the key 'dev'
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing.
        # This file is not committed. Place it in production deployments.
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in.
        app.config.from_mapping(test_config)

    # initialize instance of LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    # set the default login view to /login
    login_manager.login_view = 'login'

    # initialize instance of our Backend
    backend = Backend()

    # create all the endpoints required for the app
    pages.make_endpoints(app)
    login.make_endpoints(app, login_manager, backend)

    return app
