# -*- coding: utf-8 -*-
from icemac.addressbook.i18n import _
import grokcore.component as grok
import icemac.ab.importer.browser.table
import icemac.ab.importer.interfaces
import icemac.addressbook.browser.breadcrumb
import icemac.addressbook.browser.file.file
import icemac.addressbook.browser.table
import z3c.table.column
import zope.security.proxy


class ImporterBreadCrumb(
        icemac.addressbook.browser.breadcrumb.MasterdataChildBreadcrumb):
    """Breadcrumb for the importer."""

    grok.adapts(
        icemac.ab.importer.interfaces.IImporter,
        icemac.addressbook.browser.interfaces.IAddressBookLayer)

    title = _('Importer')


class Overview(icemac.addressbook.browser.table.PageletTable):
    """List of already uploaded import files + action links."""

    title = _('Files for import')
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
        return list(self.context.values())


def provide_IImportFile(file):
    """Provide the `IImportFile` marker interface."""
    zope.interface.directlyProvides(
        file, zope.security.proxy.removeSecurityProxy(
            icemac.ab.importer.interfaces.IImportFile))


class Add(icemac.addressbook.browser.file.file.Add):
    """Add a file with the `IImportFile` marker interface."""

    interface = icemac.ab.importer.interfaces.IImportFile

    def create(self, data):
        file = icemac.addressbook.utils.create_obj(self.class_)
        provide_IImportFile(file)
        icemac.addressbook.browser.file.file.update_blob(
            self.widgets['data'], file)
        return file
