import os

from flask import Flask
from flask_api import FlaskAPI


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app = FlaskAPI(__name__)
    #app.config['JSON_AS_ASCII'] = False
    app.config.from_mapping(
        SECRET_KEY='dev',
        JSON_AS_ASCII=False,
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import device
    app.register_blueprint(device.bp)
    return app
