# -*- coding: utf-8 -*-
from icemac.addressbook.i18n import _
import icemac.addressbook.browser.base
import zope.component
import icemac.ab.importer.interfaces


class Readers(icemac.addressbook.browser.base.FlashView):
    """List the known readers."""

    title = _('Registered import file readers')

    def readers(self):
        readers = zope.component.getAdapters(
            (None, ), icemac.ab.importer.interfaces.IImportFileReader)
        for name, reader in readers:
            yield reader.title
