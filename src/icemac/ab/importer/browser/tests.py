# -*- coding: latin-1 -*-
# Copyright (c) 2008-2009 Michael Howitz
# See also LICENSE.txt
# $Id$

import icemac.addressbook.testing
import zope.app.testing.functional


zope.app.testing.functional.defineLayer('ImporterLayer', zcml='ftesting.zcml')


def test_suite():
    return icemac.addressbook.testing.FunctionalDocFileSuite(
        "importer.txt",
        "wizard.txt",
        "masterdata.txt",
        package='icemac.ab.importer.browser',
        layer=ImporterLayer,
        )
