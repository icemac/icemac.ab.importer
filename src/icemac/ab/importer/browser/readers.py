# -*- coding: utf-8 -*-
# Copyright (c) 2009-2010 Michael Howitz
# See also LICENSE.txt

import zope.component
import icemac.ab.importer.interfaces


class Readers(object):

    def readers(self):
        readers =  zope.component.getAdapters(
            (None, ), icemac.ab.importer.interfaces.IImportFileReader)
        for name, reader in readers:
            yield reader.title
