# -*- coding: utf-8 -*-
# Copyright (c) 2009-2010 Michael Howitz
# See also LICENSE.txt

import icemac.ab.importer.interfaces
import zope.component
import zope.interface


class BaseReader(object):
    """Base class for import file readers."""

    zope.interface.implements(icemac.ab.importer.interfaces.IImportFileReader)
    zope.component.adapts(None)

    title = None
    file = None

    def __init__(self, ignored=None):
        """Adapter look-up requires an argument, but we do not need one."""

    @classmethod
    def open(cls, file_handle):
        reader = cls()
        reader.file = file_handle
        return reader

    @classmethod
    def canRead(cls, file_handle):
        try:
            reader = cls.open(file_handle)
            return bool(list(reader.getFieldNames()))
        except:
            return False

    def __del__(self):
        if self.file is not None:
            self.file.close()

    def getFieldNames(self):
        raise NotImplementedError

    def getFieldSamples(self, field_name):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError
