# -*- coding: utf-8 -*-
# Copyright (c) 2008-2012 Michael Howitz
# See also LICENSE.txt

import icemac.ab.importer.interfaces
import unittest
import zope.interface.verify
import icemac.ab.importer.reader.base


class BaseReaderTest(unittest.TestCase):
    "Base class for reader tests."

    def test_interfaces(self):
        zope.interface.verify.verifyObject(
            icemac.ab.importer.interfaces.IImportFileReader,
            icemac.ab.importer.reader.base.BaseReader())

    def test_canRead_exception_in_open(self):
        class Reader(icemac.ab.importer.reader.base.BaseReader):

            @classmethod
            def open(cls, file):
                raise Exception()

        self.assertEqual(False, Reader.canRead(None))

    def test_canRead_exception_in_getFieldNames(self):
        class Reader(icemac.ab.importer.reader.base.BaseReader):

            def getFieldNames(self):
                raise Exception()

        self.assertEqual(False, Reader.canRead(None))

    def test_canRead_getFieldNames_returns_empty_list(self):
        class Reader(icemac.ab.importer.reader.base.BaseReader):

            def getFieldNames(self):
                return []

        self.assertEqual(False, Reader.canRead(None))

    def test_canRead_getFieldNames_returns_nonempty_list(self):
        class Reader(icemac.ab.importer.reader.base.BaseReader):

            def getFieldNames(self):
                return ['sdfg']

        self.assertEqual(True, Reader.canRead(None))

    def test_getFieldNames(self):
        self.assertRaises(
            NotImplementedError,
            icemac.ab.importer.reader.base.BaseReader().getFieldNames)

    def test_getFieldSamples(self):
        self.assertRaises(
            NotImplementedError,
            icemac.ab.importer.reader.base.BaseReader().getFieldSamples, None)

    def test___iter__(self):
        self.assertRaises(
            NotImplementedError,
            icemac.ab.importer.reader.base.BaseReader().__iter__)
