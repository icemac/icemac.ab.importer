# Copyright (c) 2008-2009 Michael Howitz
# See also LICENSE.txt

import icemac.ab.importer.install
import icemac.addressbook.addressbook
import unittest
import zope.component.globalregistry
import zope.container.contained
import zope.traversing.adapters


class TestInstall(unittest.TestCase):

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
        self.ab = icemac.addressbook.addressbook.AddressBook()
        gsm = zope.component.globalregistry.getGlobalSiteManager()
        gsm.registerAdapter(zope.traversing.adapters.Traverser,
                            required=[zope.interface.Interface])
        gsm.registerAdapter(zope.traversing.adapters.DefaultTraversable,
                            required=[zope.interface.Interface])
        gsm.registerAdapter(zope.container.contained.NameChooser,
                            required=[zope.interface.Interface])

    def tearDown(self):
        gsm = zope.component.globalregistry.getGlobalSiteManager()
        gsm.unregisterAdapter(zope.traversing.adapters.Traverser,
                              required=[zope.interface.Interface])
        gsm.unregisterAdapter(zope.traversing.adapters.DefaultTraversable,
                              required=[zope.interface.Interface])
        gsm.unregisterAdapter(zope.container.contained.NameChooser,
                              required=[zope.interface.Interface])

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
