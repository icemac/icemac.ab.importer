# -*- coding: utf-8 -*-
# Copyright (c) 2009 Michael Howitz
# See also LICENSE.txt

from icemac.addressbook.i18n import MessageFactory as _
import icemac.ab.importer.browser.wizard.base
import icemac.ab.importer.source
import zope.interface
import zope.schema


class IReadersList(zope.interface.Interface):
    "A list of import readers which are able to read the file."

    reader = zope.schema.Choice(
        title=_(u'Import file reader'),
        source=icemac.ab.importer.source.Importers())


class ChooseReader(
    icemac.ab.importer.browser.wizard.base.FileSessionStorageStep):

    interface = IReadersList
    label = _(u'Choose reader')

    @property
    def showBackButton(self):
        """Back button condition."""
        return True

    def doBack(self, action):
        """Process back action and return True on sucess."""
        self.getContent()['edit_file_available'] = True
        return super(ChooseReader, self).doBack(action)

