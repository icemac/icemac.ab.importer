# Copyright (c) 2014 Michael Howitz
# See also LICENSE.txt
import icemac.ab.importer.interfaces
import icemac.addressbook.browser.menus.menu


importer_views = icemac.addressbook.browser.menus.menu.SelectMenuItemOn(
    icemac.ab.importer.interfaces.IImporter,
    icemac.ab.importer.interfaces.IImportFile)
