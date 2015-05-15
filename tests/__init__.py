#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of evesso.
# https://github.com/TomNeyland/eve-sso

# Licensed under the TBD license:
# http://www.opensource.org/licenses/TBD-license
# Copyright (c) 2015, Tom Neyland <tcneyland+github@gmail.com>


from preggy import expect
import evesso
from evesso import models

from .base import TestCase


class ExportsTestCase(TestCase):

    def test_evesso_exports(self):
        expect(evesso.create_app).not_to_be_null()
        expect(evesso.utils).not_to_be_null()
        expect(evesso.db).not_to_be_null()

    def test_evesso_model_exports(self):
        expect(models.Character).not_to_be_null()
        expect(models.Chatroom).not_to_be_null()
        expect(models.ChatroomCharacters).not_to_be_null()
        expect(models.CrestAuthorization).not_to_be_null()
        expect(models.Event).not_to_be_null()
        expect(models.Group).not_to_be_null()
        expect(models.GroupUser).not_to_be_null()
        expect(models.GroupAuthLevel).not_to_be_null()
        expect(models.GroupUser).not_to_be_null()
