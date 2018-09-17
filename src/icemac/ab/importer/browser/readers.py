# -*- coding: utf-8 -*-
from icemac.addressbook.i18n import _
import icemac.ab.importer.interfaces
import icemac.addressbook.browser.base
import zope.component


class Readers(icemac.addressbook.browser.base.FlashView):
    """List the known readers."""

    title = _('Supported import file formats')

    def readers(self):
        readers = zope.component.getAdapters(
            (None, ), icemac.ab.importer.interfaces.IImportFileReader)
        for name, reader in readers:
            yield reader.title
