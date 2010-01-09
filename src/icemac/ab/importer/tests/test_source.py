# -*- coding: utf-8 -*-
# Copyright (c) 2009-2010 Michael Howitz
# See also LICENSE.txt

import StringIO
import icemac.ab.importer.interfaces
import icemac.ab.importer.reader.base
import icemac.ab.importer.source
import unittest
import zope.component
import zope.component.globalregistry
import zope.interface
import zope.interface.verify


class DummyReader(icemac.ab.importer.reader.base.BaseReader):

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

    def getFieldNames(self):
        self.file.seek(0)
        data = self.file.read()
        if data.startswith('<?xml'):
            raise ValueError('No XML!')
        return ['field1']


class DummyImportFile(object):

    zope.interface.implements(icemac.ab.importer.interfaces.IImportFile)

    def __init__(self, data):
        self.data = data

    def openDetached(self):
        return StringIO.StringIO(self.data)


class TestSource(unittest.TestCase):

    def setUp(self):
        self.source = icemac.ab.importer.source.Importers()
        gsm = zope.component.globalregistry.getGlobalSiteManager()
        gsm.registerAdapter(DummyReader, name='dummy')
        gsm.registerAdapter(NoXMLReader, name='no-xml')

    def tearDown(self):
        gsm = zope.component.globalregistry.getGlobalSiteManager()
        gsm.unregisterAdapter(DummyReader, name='dummy')
        gsm.unregisterAdapter(NoXMLReader, name='no-xml')

    def test_dummy_reader(self):
        zope.interface.verify.verifyObject(
            icemac.ab.importer.interfaces.IImportFileReader,
            DummyReader())

    def test_noxml_reader(self):
        zope.interface.verify.verifyObject(
            icemac.ab.importer.interfaces.IImportFileReader,
            NoXMLReader())

    def test_getValue__txt_file(self):
        file = DummyImportFile('text')
        self.assertEqual([u'dummy', u'no-xml'],
                         list(self.source.factory.getValues(file)))

    def test_getValue__xml_file(self):
        file = DummyImportFile('<?xml ...')
        self.assertEqual([u'dummy'],
                         list(self.source.factory.getValues(file)))

    def test_getTitle(self):
        file = DummyImportFile('text')
        self.assertEqual(u'Dummy Reader',
                         self.source.factory.getTitle(file, 'dummy'))
        self.assertEqual(u'Dummy Reader',
                         self.source.factory.getTitle(file, 'no-xml'))
