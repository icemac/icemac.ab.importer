# -*- coding: utf-8 -*-
import zope.component
import icemac.ab.importer.interfaces


class Readers(object):
    """List the known readers."""

    def readers(self):
        readers = zope.component.getAdapters(
            (None, ), icemac.ab.importer.interfaces.IImportFileReader)
        for name, reader in readers:
            yield reader.title
