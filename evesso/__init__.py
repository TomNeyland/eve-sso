import sys
from flask import Flask, current_app
from flask.ext.sqlalchemy import SQLAlchemy

from evesso import utils

from evesso.sso import oauth, eve_oauth

import logging
log = logging.getLogger(__name__)

db = SQLAlchemy()


def setup_logging(app=current_app):
    logging.basicConfig()

    log.setLevel(app.config.get('LOG_LEVEL', logging.ERROR))

    flask_oauthlib_log = logging.getLogger('flask_oauthlib')
    flask_oauthlib_log.addHandler(logging.StreamHandler(sys.stdout))
    flask_oauthlib_log.setLevel(app.config.get('LOG_LEVEL', logging.DEBUG))

    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


def create_app(config=None):
    log.debug('creating app with config: %s', config)

    import models
    from evesso.auth import auth, login_manager
    from evesso.chat import socketio

    app = Flask(__name__, instance_relative_config=True, static_folder='../static/build/app/', static_url_path='/static')
    app.config.from_pyfile(config)

    setup_logging(app)

    db.init_app(app)
    app.db = db
    db.scoped_session = scoped_session


    socketio.init_app(app)
    app.socketio = socketio


    oauth.init_app(app)
    app.eve_oauth = eve_oauth


    login_manager.init_app(app)
    app.login_manager = login_manager


    app.register_blueprint(auth)

    return app


def scoped_session():
    pass

