# -*- coding: utf-8 -*-
import zope.container.btree
import zope.interface
import icemac.ab.importer.interfaces


class Importer(zope.container.btree.BTreeContainer):
    """Importer containing files for import."""

    zope.interface.implements(icemac.ab.importer.interfaces.IImporter)
