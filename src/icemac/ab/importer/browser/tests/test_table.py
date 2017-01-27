# -*- coding: utf-8 -*-
from datetime import datetime
from icemac.ab.importer.browser.table import ModifiedColumnLocalTime
from pytz import utc
from zope.i18n.locales import LocaleTimeZone
from zope.publisher.browser import TestRequest as ExampleRequest


class DummyDC(object):
    """Dummy dublin core object."""

    modified = datetime(2003, 5, 3, 11, 12, 13, tzinfo=utc)


def test_table__ModifiedColumnLocalTime__getValue__1():
    """It returns an empty string for `None`."""
    column = ModifiedColumnLocalTime(None, ExampleRequest(), None)
    assert u'' == column.getValue(None)


def test_table__ModifiedColumnLocalTime__getValue__2():
    """It returns None if `modified` is `None`."""
    column = ModifiedColumnLocalTime(None, ExampleRequest(), None)
    dc = DummyDC()
    dc.modified = None
    assert column.getValue(dc) is None


def test_table__ModifiedColumnLocalTime__getValue__3():
    """It returns modified in UTC if nothing else is defined."""
    column = ModifiedColumnLocalTime(None, ExampleRequest(), None)
    dc = DummyDC()
    value = column.getValue(dc)
    assert dc.modified == value
    assert 'UTC' == value.tzinfo.zone


def test_table__ModifiedColumnLocalTime__getValue__4():
    """It returns modified in local timezone if it is set."""
    column = ModifiedColumnLocalTime(None, ExampleRequest(), None)
    try:
        column.request.locale.dates.timezones[u'Europe/Berlin'] = (
            LocaleTimeZone(u'Europe/Berlin'))
        dc = DummyDC()
        value = column.getValue(dc)
        assert dc.modified == value
        assert 'Europe/Berlin' == value.tzinfo.zone
    finally:
        # timezones seems to store information globally
        ExampleRequest().locale.dates.timezones.pop(u'Europe/Berlin', None)
