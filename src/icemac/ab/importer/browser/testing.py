# Copyright (c) 2008-2011 Michael Howitz
# See also LICENSE.txt
# $Id$

import zope.app.wsgi.testlayer
import icemac.ab.importer.browser
import icemac.addressbook.testing

ImporterLayer = zope.app.wsgi.testlayer.BrowserLayer(
    icemac.ab.importer.browser)
ImporterLayer.__bases__ = (icemac.addressbook.testing.FunctionalLayer,)
