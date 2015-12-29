# -*- coding: utf-8 -*-
from icemac.addressbook.i18n import _
import icemac.ab.importer.browser.table
import icemac.ab.importer.interfaces
import icemac.addressbook.browser.file.file
import icemac.addressbook.browser.table
import z3c.table.column
import zope.security.proxy


class Overview(icemac.addressbook.browser.table.PageletTable):
    """List of already uploaded import files + action links."""

    no_rows_message = _(u'No import files uploaded, yet.')

    def setUpColumns(self):
        return [
            z3c.table.column.addColumn(
                self, icemac.addressbook.browser.table.TitleLinkColumn,
                'file', weight=1),
            z3c.table.column.addColumn(
                self, z3c.table.column.GetAttrColumn, 'mimeType', weight=2,
                header=_(u'MIME type'), attrName='mimeType'),
            z3c.table.column.addColumn(
                self, icemac.addressbook.browser.table.TruncatedContentColumn,
                'notes', weight=3, header=_(u'Notes'), attrName='notes',
                length=50),
            z3c.table.column.addColumn(
                self, icemac.ab.importer.browser.table.ModifiedColumnLocalTime,
                'modified', weight=5),
            z3c.table.column.addColumn(
                self, icemac.addressbook.browser.table.DeleteLinkColumn,
                'delete', weigth=6),
            z3c.table.column.addColumn(
                self, z3c.table.column.LinkColumn, 'import', weight=200,
                header=_(u''), linkContent=_(u'Import'),
                linkName='@@import')]

    @property
    def values(self):
        return self.context.values()


def provide_IImportFile(file):
    """Provide the `IImportFile` marker interface."""
    zope.interface.directlyProvides(
        file, zope.security.proxy.removeSecurityProxy(
            icemac.ab.importer.interfaces.IImportFile))


class Add(icemac.addressbook.browser.file.file.Add):
    """Add a file with the `IImportFile` marker interface."""

    def create(self, data):
        file = super(Add, self).create(data)
        provide_IImportFile(file)
        return file
