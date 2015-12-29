# -*- coding: utf-8 -*-
from icemac.ab.importer.interfaces import IImportFileReader
from icemac.ab.importer.source import Importers
import StringIO
import icemac.ab.importer.interfaces
import icemac.ab.importer.reader.base
import icemac.ab.importer.source
import pytest
import zope.component
import zope.component.globalregistry
import zope.interface
import zope.interface.verify


class DummyReader(icemac.ab.importer.reader.base.BaseReader):
    """Dummy reader implementation."""

    title = u'Dummy Reader'

    def getFieldNames(self):
        """Get the names of the fields in the file."""
        # canRead requires at least a field name to return True
        return ['field1']

    def getFieldSamples(self, field_name):
        """Get sample values for a field."""
        return []

    def __iter__(self):
        """Iterate over the file."""


class NoXMLReader(DummyReader):
    """A dummy reader implementation which does not like XML files."""

    def getFieldNames(self):
        self.file.seek(0)
        data = self.file.read()
        if data.startswith('<?xml'):
            raise ValueError('No XML!')
        return ['field1']


class DummyImportFile(object):
    """A dummy import file implemention."""

    zope.interface.implements(icemac.ab.importer.interfaces.IImportFile)

    def __init__(self, data):
        self.data = data

    def openDetached(self):
        return StringIO.StringIO(self.data)


@pytest.yield_fixture('module', autouse=True)
def dummy_readers(zcmlS):
    """Register some dummy readers for the tests."""
    gsm = zope.component.globalregistry.getGlobalSiteManager()
    gsm.registerAdapter(DummyReader, name='dummy')
    gsm.registerAdapter(NoXMLReader, name='no-xml')
    yield
    gsm.unregisterAdapter(DummyReader, name='dummy')
    gsm.unregisterAdapter(NoXMLReader, name='no-xml')


def test_test_source__1():
    """Verify the dummy objects fulfilling thier interfaces."""
    assert zope.interface.verify.verifyObject(IImportFileReader, DummyReader())
    assert zope.interface.verify.verifyObject(IImportFileReader, NoXMLReader())


def test_source__Importers__getValue__1():
    """It returns all readers capable to read text files."""
    file = DummyImportFile('text')
    assert [u'dummy',
            u'csv-commaseparated-utf8-isodate',
            u'no-xml'] == list(Importers().factory.getValues(file))


def test_source__Importers__getValue__2():
    """It returns all readers capable to read XML files."""
    file = DummyImportFile('<?xml ...')
    assert ([u'dummy', u'csv-commaseparated-utf8-isodate'] ==
            list(Importers().factory.getValues(file)))


def test_source__Importers__getTitle__1():
    """It returns the title of the reader."""
    file = DummyImportFile('text')
    assert u'Dummy Reader' == Importers().factory.getTitle(file, 'dummy')
    assert u'Dummy Reader' == Importers().factory.getTitle(file, 'no-xml')
