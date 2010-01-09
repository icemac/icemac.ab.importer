# -*- coding: utf-8 -*-
# Copyright (c) 2009-2010 Michael Howitz
# See also LICENSE.txt

from icemac.addressbook.i18n import MessageFactory as _
import icemac.addressbook.browser.table
import z3c.table.column
import icemac.ab.importer.browser.table


class Overview(icemac.addressbook.browser.table.PageletTable):

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
                linkName='@@import'),
            ]

    @property
    def values(self):
        return self.context.values()
