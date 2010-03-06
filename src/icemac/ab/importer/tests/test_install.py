# Copyright (c) 2008-2010 Michael Howitz
# See also LICENSE.txt

import icemac.ab.importer.install
import icemac.addressbook.addressbook
import icemac.addressbook.testing
import zope.component.globalregistry
import zope.container.contained
import zope.traversing.adapters


class TestInstall(icemac.addressbook.testing.FunctionalTestCase):

    def assertLocalUtility(self, ab, iface):
        self.assertTrue(
            icemac.addressbook.addressbook.utility_locally_registered(ab, iface)
            )

    def assertAttribute(self, ab, attribute, iface):
        self.assertTrue(iface.providedBy(getattr(ab, attribute)))
        self.assertLocalUtility(ab, iface)

    def check_addressbook(self, ab):
        self.assertAttribute(
            ab, 'importer', icemac.ab.importer.interfaces.IImporter)

    def setUp(self):
        super(TestInstall, self).setUp()
        root = self.getRootFolder()
        root['ab'] = self.ab = icemac.addressbook.utils.create_obj(
            icemac.addressbook.addressbook.AddressBook)

    def test_create(self):
        icemac.addressbook.addressbook.create_address_book_infrastructure(
            self.ab)
        icemac.ab.importer.install.install_importer(self.ab)
        self.check_addressbook(self.ab)

    def test_recall_create(self):
        icemac.addressbook.addressbook.create_address_book_infrastructure(
            self.ab)
        icemac.ab.importer.install.install_importer(self.ab)
        icemac.ab.importer.install.install_importer(self.ab)
        self.check_addressbook(self.ab)
