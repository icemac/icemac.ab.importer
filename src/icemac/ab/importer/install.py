# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012 Michael Howitz
# See also LICENSE.txt

import icemac.ab.importer.importer
import icemac.ab.importer.interfaces
import zope.component


@zope.component.adapter(
    icemac.addressbook.addressbook.AddressBookCreated)
def install_importer(event):
    "Install the importer in the newly created addressbook."
    address_book = event.address_book
    icemac.addressbook.addressbook.create_and_register(
        address_book, 'importer', icemac.ab.importer.importer.Importer,
        icemac.ab.importer.interfaces.IImporter)
