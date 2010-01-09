# -*- coding: utf-8 -*-
# Copyright (c) 2009-2010 Michael Howitz
# See also LICENSE.txt

import icemac.ab.importer.interfaces
import zc.sourcefactory.contextual
import zope.component


class Importers(zc.sourcefactory.contextual.BasicContextualSourceFactory):
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
