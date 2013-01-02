# -*- coding: utf-8 -*-
# Copyright (c) 2008-2012 Michael Howitz
# See also LICENSE.txt
"""Initial generation."""


import icemac.ab.importer.install
import icemac.addressbook.generations.utils


@icemac.addressbook.generations.utils.evolve_addressbooks
def evolve(address_book):
    """Installs the importer into each existing address book."""
    icemac.ab.importer.install.install_importer(address_book)
