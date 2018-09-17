# -*- coding: utf-8 -*-
from icemac.addressbook.i18n import _
import icemac.ab.importer.browser.wizard.base
import icemac.ab.importer.source
import zope.interface
import zope.schema


class IReaderSettings(zope.interface.Interface):
    """Reader Setttings."""

    reader = zope.schema.Choice(
        title=_(u'Import file format'),
        description=_(
            "If the drop-down is empty the file's format is not supported."),
        source=icemac.ab.importer.source.Importers())

    entries_number = zope.schema.Int(
        title=_('person sub-entities'),
        description=_(
            'This is the maximum number per person of postal addresses, phone'
            ' numbers, e-mail addresses resp. homepage addresses the import'
            ' file contains.'),
        min=1, max=9, default=1)


class ReaderSettings(
        icemac.ab.importer.browser.wizard.base.FileSessionStorageStep):
    """Step to set the reader and the number of entries."""

    interface = IReaderSettings
    title = label = _(u'File format settings')

    @property
    def showBackButton(self):
        """Back button condition."""
        return True

    def doBack(self, action):
        """Process back action and return True on success."""
        self.getContent()['edit_file_available'] = True
        return super(ReaderSettings, self).doBack(action)
