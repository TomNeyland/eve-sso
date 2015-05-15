#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of evesso.
# https://github.com/TomNeyland/resource-alchemy

# Licensed under the TBD license:
# http://www.opensource.org/licenses/TBD-license
# Copyright (c) 2015, Tom Neyland <tcneyland+github@gmail.com>

from preggy import expect

from evesso import __version__
from tests.base import TestCase


class VersionTestCase(TestCase):

    def test_has_proper_version(self):
        expect(__version__).to_equal('0.1.0')
