#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of evesso.
# https://github.com/TomNeyland/resource-alchemy

# Licensed under the TBD license:
# http://www.opensource.org/licenses/TBD-license
# Copyright (c) 2015, Tom Neyland <tcneyland+github@gmail.com>

from unittest import TestCase as PythonTestCase


class TestCase(PythonTestCase):
    pass


class TestObj(object):

    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)
