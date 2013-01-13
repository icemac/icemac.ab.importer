# Copyright (c) 2008-2013 Michael Howitz
# See also LICENSE.txt
import icemac.addressbook.testing
import icemac.ab.importer.testing


def test_suite():
    return icemac.addressbook.testing.DocFileSuite(
        "importer.txt",
        "masterdata.txt",
        package='icemac.ab.importer.browser',
        layer=icemac.ab.importer.testing.TEST_BROWSER_LAYER,
        )
