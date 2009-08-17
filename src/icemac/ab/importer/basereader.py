# -*- coding: utf-8 -*-
# Copyright (c) 2009 Michael Howitz
# See also LICENSE.txt

import icemac.ab.importer.interfaces
import zc.sourcefactory.contextual
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


class Source(zc.sourcefactory.contextual.BasicContextualSourceFactory):
    """Source of readers which are able to read the blob."""

    def getValues(self, context):
        # Get all import file readers
        adapters =  zope.component.getAdapters(
            (None, ), icemac.ab.importer.interfaces.IImportFileReader)
        file = icemac.ab.importer.interfaces.IImportFile(context)

        # return only the readers which are able to read the import file
        for name, adapter in adapters:
            if adapter.__class__.canRead(file.openDetached()):
                yield name

    def getTitle(self, context, value):
        adapter = zope.component.getAdapter(
            None, icemac.ab.importer.interfaces.IImportFileReader,
            name=value)

        return adapter.title
