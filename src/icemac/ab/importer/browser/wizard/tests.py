# -*- coding: latin-1 -*-
# Copyright (c) 2008-2009 Michael Howitz
# See also LICENSE.txt
# $Id$

import icemac.addressbook.testing
import icemac.ab.importer.browser.testing

def test_suite():
    return icemac.addressbook.testing.FunctionalDocFileSuite(
        "constraints.txt",
        "edgecases.txt",
        "keywords.txt",
        "wizard.txt",
        package='icemac.ab.importer.browser.wizard',
        layer=icemac.ab.importer.browser.testing.ImporterLayer,
        )
