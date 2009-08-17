# -*- coding: utf-8 -*-
# Copyright (c) 2009 Michael Howitz
# See also LICENSE.txt

import icemac.ab.importer.testing
# import gocept.reference.interfaces
import icemac.ab.file.tests
import icemac.ab.importer.interfaces
import icemac.ab.importer.readers.base
# import icemac.ab.importer.readers.xls
import icemac.ab.testing
import zope.component.globalregistry
import zope.interface.verify


class DummyReader(icemac.ab.importer.readers.base.BaseReader):

    title = u'Dummy Reader'

    def getFieldNames(self):
        """Get the names of the fields in the file."""
        return []

    def getFieldSamples(self, field_name):
        """Get sample values for a field."""
        return []

    def __iter__(self):
        """Iterate over the file."""


# class DummyReferenceManager(object):

#     def is_referenced(self, dummy):
#         return False

dummy_reference_manager = DummyReferenceManager()

class TestSource(icemac.ab.file.tests.Base,
                 icemac.ab.testing.FunctionalTestCase):

    file_key = 'import_file'

    def setUp(self):
        super(TestSource, self).setUp()
        self.source = icemac.ab.importer.readers.base.Source()
        gsm = zope.component.globalregistry.getGlobalSiteManager()
        gsm.registerAdapter(DummyReader, name='dummy')
        gsm.registerAdapter(
            icemac.ab.importer.readers.xls.XLSReader, name='xls')
        gsm.registerUtility(
            dummy_reference_manager,
            provided=gocept.reference.interfaces.IReferenceManager)

    def tearDown(self):
        super(TestSource, self).tearDown()
        root = self.getRootFolder()
        if self.file_key in root.keys():
            del root[self.file_key]
        gsm = zope.component.globalregistry.getGlobalSiteManager()
        gsm.unregisterAdapter(DummyReader, name='dummy')
        gsm.unregisterAdapter(
            icemac.ab.importer.readers.xls.XLSReader, name='xls')
        gsm.unregisterUtility(
            dummy_reference_manager,
            provided=gocept.reference.interfaces.IReferenceManager)

    def set_file(self, file_name):
        """Save the file contents in a blob, stored on self.file."""
        self.getRootFolder()[self.file_key] = self.file
        zope.interface.alsoProvides(
            self.file, icemac.ab.importer.interfaces.IImportFile)
        self.file.data = icemac.ab.importer.testing.getFileHandle(
            file_name).read()
        # commit as openDetached expects a committed blob
        self.commit()

    def test_dummy_reader(self):
        zope.interface.verify.verifyObject(
            icemac.ab.importer.interfaces.IImportFileReader,
            DummyReader())

    def test_getValue__xls_file(self):
        self.set_file('xls_short.xls')
        self.assertEqual([u'dummy', u'xls'],
                         list(self.source.factory.getValues(self.file)))

    def test_getValue__txt_file(self):
        self.set_file('dummy.txt')
        self.assertEqual([u'dummy'],
                         list(self.source.factory.getValues(self.file)))

    def test_getTitle(self):
        self.set_file('xls_short.xls')
        self.assertEqual(u'Dummy Reader',
                         self.source.factory.getTitle(self.file, 'dummy'))
