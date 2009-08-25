# -*- coding: utf-8 -*-
# Copyright (c) 2009 Michael Howitz
# See also LICENSE.txt

import icemac.ab.importer.importer
import icemac.ab.importer.interfaces
import icemac.addressbook.interfaces
import zope.component
import zope.container.interfaces


@zope.component.adapter(
    icemac.addressbook.interfaces.IAddressBook,
    zope.container.interfaces.IObjectAddedEvent)
def install_importer(addressbook, event=None):
    "Install the importer in the newly created addressbook."
    icemac.addressbook.addressbook.create_and_register(
        addressbook, 'importer', icemac.ab.importer.importer.Importer,
        icemac.ab.importer.interfaces.IImporter)