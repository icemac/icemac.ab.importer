# Copyright (c) 2008-2013 Michael Howitz
# See also LICENSE.txt

import icemac.addressbook.testing
import icemac.ab.importer.testing


def test_suite():
    return icemac.addressbook.testing.DocFileSuite(
        "constraints.txt",
        "edgecases.txt",
        "keywords.txt",
        "multientries.txt",
        "wizard.txt",
        "userfields.txt",
        package='icemac.ab.importer.browser.wizard',
        layer=icemac.ab.importer.testing.TEST_BROWSER_LAYER,
        )
