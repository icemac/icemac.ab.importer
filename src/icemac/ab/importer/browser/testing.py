# Copyright (c) 2008-2011 Michael Howitz
# See also LICENSE.txt
# $Id$

import icemac.ab.importer.browser
import icemac.addressbook.testing

class _ImporterLayer(icemac.addressbook.testing._ZCMLAndZODBLayer):

    package = icemac.ab.importer.browser
    defaultBases = (icemac.addressbook.testing.WSGI_TEST_BROWSER_LAYER,)


ImporterLayer = _ImporterLayer(name='ImporterLayer')
