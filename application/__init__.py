# application/__init__.py

import logging
from os import environ
from flask import Flask

logging.basicConfig(filename='error.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def create_app():
    '''Get application set up'''

    app = Flask(__name__)

    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = environ.get('SECRET_KEY')

    from application.main.routes import main
    app.register_blueprint(main)


    return app
