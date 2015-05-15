#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of evesso.
# https://github.com/TomNeyland/eve-sso

# Licensed under the TBD license:
# http://www.opensource.org/licenses/TBD-license
# Copyright (c) 2015, Tom Neyland <tcneyland+github@gmail.com>

from preggy import expect
import evesso

from tests.base import TestCase


class ExportsTestCase(TestCase):

    def test_evesso_exports(self):

        expect(evesso.create_app).not_to_be_null()
        expect(evesso.db).not_to_be_null()
