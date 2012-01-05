# Copyright (c) 2008-2012 Michael Howitz
# See also LICENSE.txt
# $Id$

import icemac.ab.importer.browser
import icemac.addressbook.testing
import plone.testing.zca


IMPORTER_ZCML_LAYER = plone.testing.zca.ZCMLSandbox(
    name="ImporterZCML", filename="ftesting.zcml",
    package=icemac.ab.importer.browser)


ImporterLayer = icemac.addressbook.testing._WSGITestBrowserLayer(
    bases=[icemac.addressbook.testing.WSGILayer(
        bases=[icemac.addressbook.testing._ZODBIsolatedTestLayer(
            bases=[icemac.addressbook.testing._ZODBLayer(
                bases=[icemac.addressbook.testing.ZCML_LAYER,
                       IMPORTER_ZCML_LAYER],
                name='ImporterZODBLayer')],
            name='ImporterZODBIsolatedTestLayer')],
        name='ImporterWSGILayer')],
    name='ImporterLayer')
