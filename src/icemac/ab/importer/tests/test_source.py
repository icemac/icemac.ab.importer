# -*- coding: utf-8 -*-
from icemac.ab.importer.interfaces import IImportFileReader
from icemac.ab.importer.source import Importers
import icemac.ab.importer.interfaces
import icemac.ab.importer.reader.base
import icemac.ab.importer.source
import io
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

    def __iter__(self):
        """Iterate over the file."""


class NoXMLReader(DummyReader):
    """A dummy reader implementation which does not like XML files."""

    def getFieldNames(self):
        self.file.seek(0)
        data = self.file.read()
        if data.startswith(b'<?xml'):
            raise ValueError('No XML!')
        return ['field1']


@zope.interface.implementer(icemac.ab.importer.interfaces.IImportFile)
class DummyImportFile(object):
    """A dummy import file implemention."""

    def __init__(self, data):
        self.data = data.encode('utf-8')

    def openDetached(self):
        return io.BytesIO(self.data)


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
    assert set([
        u'dummy',
        u'csv-commaseparated-utf8-isodate',
        u'no-xml']) == set(Importers().factory.getValues(file))


def test_source__Importers__getValue__2():
    """It returns all readers capable to read XML files."""
    file = DummyImportFile('<?xml ...')
    assert (set([u'dummy', u'csv-commaseparated-utf8-isodate']) ==
            set(Importers().factory.getValues(file)))


def test_source__Importers__getTitle__1():
    """It returns the title of the reader."""
    file = DummyImportFile('text')
    assert u'Dummy Reader' == Importers().factory.getTitle(file, 'dummy')
    assert u'Dummy Reader' == Importers().factory.getTitle(file, 'no-xml')
