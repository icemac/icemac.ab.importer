# -*- coding: utf-8 -*-
# Copyright (c) 2008-2010 Michael Howitz
# See also LICENSE.txt

import datetime
import icemac.ab.importer.interfaces
import os.path
import sys
import unittest
import zope.interface.verify


class ReaderTest(unittest.TestCase):
    "Test class for readers."

    reader_class = None # reference to the reader's class object
    import_file = None # name of the longer import file
    import_file_short = None # name of the shorter import file

    def getFileHandle(self, file_name=None):
        base_path = sys.modules[self.reader_class.__module__].__file__
        if file_name is None:
            file_name = self.import_file
        return file(os.path.join(
                os.path.dirname(base_path), 'tests', 'data', file_name))

    def getReader(self, import_file=None):
        return self.reader_class.open(self.getFileHandle(import_file))

    def test_interfaces(self):
        zope.interface.verify.verifyObject(
            icemac.ab.importer.interfaces.IImportFileReader,
            self.getReader())

    def test_getFieldNames(self):
        field_names = list(self.getReader().getFieldNames())
        self.assertEqual([u'last name', u'firstname', u'birth_date'],
                         field_names)
        self.assert_(isinstance(field_names[0], unicode))
        self.assert_(isinstance(field_names[1], unicode))
        self.assert_(isinstance(field_names[2], unicode))

    def test_getFieldSamples_firstname(self):
        samples = list(self.getReader().getFieldSamples(u'firstname'))
        self.assertEqual([u'Andreas', u'Hanna', u'Jens'], samples)
        self.assert_(isinstance(samples[0], unicode))
        self.assert_(isinstance(samples[1], unicode))
        self.assert_(isinstance(samples[2], unicode))

    def test_getFieldSamples_lastname(self):
        self.assertEqual([u'Koch', u'Hula', u'Jänsen'],
                         list(self.getReader().getFieldSamples(u'last name')))

    def test_getFieldSamples_birthdate(self):
        samples = list(self.getReader().getFieldSamples(u'birth_date'))
        self.assertEqual([u'1976-01-24', u'2000-01-01', u''], samples)
        self.assert_(isinstance(samples[0], unicode))
        self.assert_(isinstance(samples[1], unicode))
        self.assert_(isinstance(samples[2], unicode))

    def test_getFieldSamples_less_than_3_samples_in_file(self):
        samples = list(self.getReader(self.import_file_short).getFieldSamples(
                u'last name'))
        self.assertEqual([u'Koch'], samples)
        self.assert_(isinstance(samples[0], unicode))

    def test_getFieldSamples_empty_string(self):
        samples = list(self.getReader(self.import_file_short).getFieldSamples(
                u'firstname'))
        self.assertEqual([u''], samples)
        self.assert_(isinstance(samples[0], unicode))

    def test___iter__(self):
        result = [[u'Koch', u'Andreas', datetime.date(1976, 1, 24)],
                  [u'Hula', u'Hanna', datetime.date(2000, 1, 1)],
                  [u'Jänsen', u'Jens', None],
                  [u'Fruma', None, datetime.date(2001, 12, 31)]]
        for index, line in enumerate(self.getReader()):
            self.assertEqual(result[index], line)
            for value in line:
                self.assert_((isinstance(value, unicode) or
                              isinstance(value, datetime.date) or
                              value is None),
                             repr(value))

    def test___iter__short(self):
        result = [[u'Koch', None, datetime.date(1976, 1, 24)]]
        for index, line in enumerate(self.getReader(self.import_file_short)):
            self.assertEqual(result[index], line)
            for value in line:
                self.assert_((isinstance(value, unicode) or
                              isinstance(value, datetime.date) or
                              value is None),
                             repr(value))
