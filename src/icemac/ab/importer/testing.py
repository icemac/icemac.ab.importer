# Copyright (c) 2012 Michael Howitz
# See also LICENSE.txt
import icemac.ab.importer
import icemac.addressbook.testing


ZCML_LAYER = icemac.addressbook.testing.ZCMLLayer(
    'Importer', __name__, icemac.ab.importer,
    bases=[icemac.addressbook.testing.ZCML_LAYER])
ZODB_LAYER = icemac.addressbook.testing.ZODBLayer(
    'Importer', ZCML_LAYER)
TEST_BROWSER_LAYER = icemac.addressbook.testing.TestBrowserLayer(
    'Importer', ZODB_LAYER)
