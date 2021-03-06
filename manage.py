from os import path
from flask import current_app
from flask.ext.script import Shell, Manager, Server, prompt_bool
import evesso.models
from evesso import db

import logging
log = logging.getLogger(__name__)

manager = Manager(evesso.create_app)
manager.add_command("runserver", Server())
manager.add_option("-c", "--config", dest="config", default='dev_config.py', required=False)


def _make_context():
    from flask import current_app

    return dict(app=current_app, drop=drop, create=create, recreate=recreate, populate=populate, **vars(evesso.models))


manager.add_command("shell", Shell(make_context=lambda: _make_context()))


@manager.command
def drop():
    "Drops database tables"
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()


@manager.command
def create(default_data=True, sample_data=False):
    "Creates database tables from sqlalchemy models"
    db.create_all()
    if default_data or sample_data:
        populate(default_data, sample_data)


@manager.command
def recreate(default_data=True, sample_data=False):
    "Recreates database tables (same as issuing 'drop' and then 'create')"
    drop()

    create(default_data, sample_data)


@manager.command
def populate(default_data=True, sample_data=False):
    "Populate database with default data"
    from fixtures import dbfixture

    if default_data:
        from fixtures import ChatroomData
        default_data = dbfixture.data(ChatroomData)
        default_data.setup()


@manager.command
def runsocket(config=''):
    from evesso import create_app, db
    from evesso.chat import socketio
    app = create_app(config)
    app.debug = False
    app.socketio.run(app, port=5000, host='0.0.0.0')


def main():
    manager.run()

if __name__ == "__main__":
    main()
