import zope.container.btree
import zope.interface
import icemac.ab.importer.interfaces


@zope.interface.implementer(icemac.ab.importer.interfaces.IImporter)
class Importer(zope.container.btree.BTreeContainer):
    """Importer containing files for import."""
