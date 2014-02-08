# -*- coding: utf-8 -*-
# Copyright (c) 2008-2014 Michael Howitz
# See also LICENSE.txt
"""Initial generation."""


import icemac.ab.importer.install
import icemac.addressbook.addressbook
import icemac.addressbook.generations.utils


@icemac.addressbook.generations.utils.evolve_addressbooks
def evolve(address_book):
    """Installs the importer into each existing address book."""
    icemac.ab.importer.install.install_importer(
        icemac.addressbook.addressbook.AddressBookCreated(address_book))
