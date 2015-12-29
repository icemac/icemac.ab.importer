import zope.interface.verify
import icemac.ab.importer.interfaces
import icemac.ab.importer.importer


def test_importer__Importer__1():
    """It fulfills the `IImporter` interface."""
    assert zope.interface.verify.verifyObject(
        icemac.ab.importer.interfaces.IImporter,
        icemac.ab.importer.importer.Importer())
