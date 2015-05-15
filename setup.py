#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of evesso.
# https://github.com/TomNeyland/eve-sso

# Licensed under the TBD license:
# http://www.opensource.org/licenses/TBD-license
# Copyright (c) 2015, Tom Neyland <tcneyland+github@gmail.com>

from setuptools import setup, find_packages
#from evesso.version import __version__

__version__ = '0.1.0'

tests_require = [
    'mock',
    'nose',
    'pylons',  # really...
    'coverage',
    'yanc',
    'preggy',
    'tox',
    'ipdb',
    'coveralls',
    'sphinx',
]

setup(
    name='evesso',
    version=__version__,
    description='Easily create SqlAlchemy backed API endpoints and resources',
    long_description='''An example flask project that uses eve-online sso for auth''',
    keywords='sqlalchemy flask eve-online crest sso oauth',
    author='Tom Neyland',
    author_email='tcneyland+github@gmail.com',
    url='https://github.com/TomNeyland/eve-sso',
    license='TBD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: TBD License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # add your dependencies here
        # remember to use 'package-name>=x.y.z,<x.y+1.0' notation (this way you get bugfixes)
        'Flask>=0.10.1',
        'Flask-Login>=0.2.11',
        'Flask-OAuth>=0.12',
        'Flask-OAuthlib>=0.9.0',
        'Flask-SQLAlchemy>=2.0',
        'Flask-Script>=2.0.5',
        'Flask-SocketIO>=0.6.0',
        'Jinja2>=2.7.3',
        'MarkupSafe>=0.23',
        'Pygments>=2.0.2',
        'SQLAlchemy>=1.0.0',
        'Werkzeug>=0.10.1',
        'argparse>=1.3.0',
        'click>=4.0',
        'dateutils>=0.6.6',
        'docopt>=0.6.2',
        'fixture>=1.5.1',
        'gevent>=1.0.1',
        'gevent-socketio>=0.3.6',
        'gevent-websocket>=0.9.3',
        'gnureadline>=6.3.3',
        'greenlet>=0.4.6',
        'httplib2>=0.9',
        'ipdb>=0.8',
        'ipython>=2.4.1',
        'itsdangerous>=0.24',
        'jedi>=0.8.1',
        'oauth2>=1.5.211',
        'oauthlib>=0.7.2',
        'pgcli>=0.16.3',
        'prompt-toolkit>=0.26',
        'psycopg2>=2.6',
        'python-dateutil>=2.4.2',
        'pytz>=2015.2',
        'requests>=2.5.1',
        'requests-oauthlib>=0.4.2',
        'simplejson>=3.6.5',
        'six>=1.9.0',
        'sqlparse>=0.1.15',
        'ujson>=1.33',
        'wcwidth>=0.1.4',
        'wsgiref>=0.1.2'
    ],
    extras_require={
        'tests': tests_require,
    },
    entry_points={
        'console_scripts': [
            # add cli scripts here in this form:
            # 'evesso=evesso.cli:main',
            'evesso=manage:main'
        ],
    },
)
