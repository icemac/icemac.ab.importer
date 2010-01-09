# -*- coding: utf-8 -*-
# Copyright (c) 2009-2010 Michael Howitz
# See also LICENSE.txt

import zope.container.btree
import zope.interface
import icemac.ab.importer.interfaces


class Importer(zope.container.btree.BTreeContainer):
    "Importer containing files for import."
    zope.interface.implements(icemac.ab.importer.interfaces.IImporter)

    file_marker_interface = icemac.ab.importer.interfaces.IImportFile
