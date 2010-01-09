# -*- coding: utf-8 -*-
# Copyright (c) 2009-2010 Michael Howitz
# See also LICENSE.txt

import unittest
import icemac.ab.importer.browser.table
import datetime
import pytz
import zope.publisher.browser


class DummyDC(object):

    modified = None


class TestModifiedColumnLocalTime(unittest.TestCase):

    def setUp(self):
        request = zope.publisher.browser.TestRequest()
        self.column = icemac.ab.importer.browser.table.ModifiedColumnLocalTime(
            None, request, None)
        self.item = DummyDC()
        self.item.modified = datetime.datetime(
            2003, 5, 3, 11, 12, 13, tzinfo=pytz.timezone('UTC'))

    def tearDown(self):
        # timezones seems to store information globally
        zope.publisher.browser.TestRequest().locale.dates.timezones.pop(
            u'Europe/Berlin', None)

    def test_no_item(self):
        self.assertEqual(u'', self.column.getValue(None))

    def test_no_value(self):
        self.item.modified = None
        self.assertEqual(u'', self.column.getValue(self.item.modified))

    def test_utc_timezone(self):
        value = self.column.getValue(self.item)
        self.assertEqual(self.item.modified, value)
        self.assertEqual('UTC', value.tzinfo.zone)

    def test_local_timezone(self):
        self.column.request.locale.dates.timezones[u'Europe/Berlin'] = (
            zope.i18n.locales.LocaleTimeZone(u'Europe/Berlin'))
        value = self.column.getValue(self.item)
        self.assertEqual(self.item.modified, value)
        self.assertEqual('Europe/Berlin', value.tzinfo.zone)
