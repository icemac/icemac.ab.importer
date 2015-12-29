# -*- coding: utf-8 -*-
import datetime
import icemac.ab.importer.interfaces
import os.path
import sys
import unittest
import zope.interface.verify


class ReaderTest(unittest.TestCase):
    """Test class for readers.

    Extend it and set the class variables to test your reader implementation.

    The import files have to be in a `test/data` directory relative to the
    importer class.
    """

    reader_class = None  # reference to the reader's class object
    import_file = None  # name of the longer import file
    import_file_short = None  # name of the shorter import file

    def getFileHandle(self, file_name=None):
        base_path = sys.modules[self.reader_class.__module__].__file__
        if file_name is None:
            file_name = self.import_file
        return file(os.path.join(
            os.path.dirname(base_path), 'tests', 'data', file_name))

    def getReader(self, import_file=None):
        return self.reader_class.open(self.getFileHandle(import_file))

    def test_Reader__interfaces__1(self):
        """It fulfills the IImportFileReader interface."""
        assert zope.interface.verify.verifyObject(
            icemac.ab.importer.interfaces.IImportFileReader,
            self.getReader())

    def test_Reader__getFieldNames__1(self):
        """It returns a list of unicode field names."""
        field_names = list(self.getReader().getFieldNames())
        assert [u'last name', u'firstname', u'birth_date'] == field_names
        assert isinstance(field_names[0], unicode)
        assert isinstance(field_names[1], unicode)
        assert isinstance(field_names[2], unicode)

    def test_Reader__getFieldSamples__1(self):
        """It returns a list of unicode field values."""
        samples = list(self.getReader().getFieldSamples(u'firstname'))
        assert [u'Andreas', u'Hanna', u'Jens'] == samples
        assert isinstance(samples[0], unicode)
        assert isinstance(samples[1], unicode)
        assert isinstance(samples[2], unicode)

    def test_Reader__getFieldSamples__2(self):
        """It is able to handle non-ASCII field values."""
        assert ([u'Koch', u'Hula', u'Jänsen'] ==
                list(self.getReader().getFieldSamples(u'last name')))

    def test_Reader__getFieldSamples__3(self):
        """It returns datetime field values as ISO unicodes."""
        samples = list(self.getReader().getFieldSamples(u'birth_date'))
        assert [u'1976-01-24', u'2000-01-01', u''] == samples
        assert isinstance(samples[0], unicode)
        assert isinstance(samples[1], unicode)
        assert isinstance(samples[2], unicode)

    def test_Reader__getFieldSamples__4(self):
        """It returns all samples if there are less than 3 in the file."""
        samples = list(self.getReader(self.import_file_short).getFieldSamples(
            u'last name'))
        assert [u'Koch'] == samples
        assert isinstance(samples[0], unicode)

    def test_Reader__getFieldSamples__5(self):
        """It returns an empty string if the only value is empty."""
        samples = list(self.getReader(self.import_file_short).getFieldSamples(
            u'firstname'))
        assert [u''] == samples
        assert isinstance(samples[0], unicode)

    def test_Reader____iter____1(self):
        """It iterates over the lines in the import file."""
        result = [[u'Koch', u'Andreas', datetime.date(1976, 1, 24)],
                  [u'Hula', u'Hanna', datetime.date(2000, 1, 1)],
                  [u'Jänsen', u'Jens', None],
                  [u'Fruma', None, datetime.date(2001, 12, 31)]]
        for index, line in enumerate(self.getReader()):
            assert result[index] == line
            for value in line:
                assert (isinstance(value, unicode) or
                        isinstance(value, datetime.date) or
                        value is None)

    def test_Reader____iter____2(self):
        """It iterates over the lines in the short import file."""
        result = [[u'Koch', None, datetime.date(1976, 1, 24)]]
        for index, line in enumerate(self.getReader(self.import_file_short)):
            assert result[index] == line
            for value in line:
                assert (isinstance(value, unicode) or
                        isinstance(value, datetime.date) or
                        value is None)
