# Copyright (c) 2008-2013 Michael Howitz
# See also LICENSE.txt

import icemac.ab.importer.install
import icemac.addressbook.addressbook
import icemac.addressbook.testing
import unittest2 as unittest


class TestInstall(unittest.TestCase,
                  icemac.addressbook.testing.InstallationAssertions):

    layer = icemac.addressbook.testing.ZODB_LAYER

    def check_addressbook(self, ab):
        self.assertAttribute(
            ab, 'importer', icemac.ab.importer.interfaces.IImporter)

    def setUp(self):
        self.ab = self.layer['addressbook']

    def test_create(self):
        icemac.addressbook.addressbook.create_address_book_infrastructure(
            self.ab)
        icemac.ab.importer.install.install_importer(
            icemac.addressbook.addressbook.AddressBookCreated(self.ab))
        self.check_addressbook(self.ab)

    def test_recall_create(self):
        icemac.addressbook.addressbook.create_address_book_infrastructure(
            self.ab)
        event = icemac.addressbook.addressbook.AddressBookCreated(self.ab)
        icemac.ab.importer.install.install_importer(event)
        icemac.ab.importer.install.install_importer(event)
        self.check_addressbook(self.ab)
