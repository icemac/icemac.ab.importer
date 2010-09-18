# -*- coding: utf-8 -*-
# Copyright (c) 2008-2010 Michael Howitz
# See also LICENSE.txt
# $Id$
"""Initial generation."""

__docformat__ = "reStructuredText"

import icemac.ab.importer.install
import icemac.addressbook.interfaces
import zope.generations.utility


def evolve(context):
    """Installs the importer into each existing address book."""
    root = zope.generations.utility.getRootFolder(context)
    address_books = zope.generations.utility.findObjectsProviding(
        root, icemac.addressbook.interfaces.IAddressBook)
    for address_book in address_books:
        icemac.ab.importer.install.install_importer(address_book, None)
