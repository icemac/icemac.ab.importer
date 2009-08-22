# -*- coding: utf-8 -*-
# Copyright (c) 2009 Michael Howitz
# See also LICENSE.txt

import icemac.ab.importer.interfaces
import zope.component
import zope.interface


class BaseReader(object):
    """Base class for import file readers."""

    zope.interface.implements(icemac.ab.importer.interfaces.IImportFileReader)
    zope.component.adapts(None)

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
            reader.getFieldNames()
        except:
            return False
        return True

    def __del__(self):
        if self.file is not None:
            self.file.close()
