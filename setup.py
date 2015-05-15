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
        # remember to use 'package-name',notation (this way you get bugfixes)
        'flask',
        'Flask-Login',
        'Flask-OAuthlib',
        'Flask-SQLAlchemy',
        'Flask-Script',
        'Flask-SocketIO',
        'Pygments',
        'SQLAlchemy',
        'dateutils',
        'fixture',
        'itsdangerous',
        'psycopg2',
        'python-dateutil',
        'pytz',
        'requests',
        'requests-oauthlib',
        'simplejson',
        'ujson',
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
