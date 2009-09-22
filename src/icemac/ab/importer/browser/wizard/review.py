# -*- coding: utf-8 -*-
# Copyright (c) 2009 Michael Howitz
# See also LICENSE.txt

from icemac.addressbook.i18n import MessageFactory as _
import icemac.addressbook.browser.table
import icemac.addressbook.interfaces
import icemac.addressbook.sources
import xml.sax.saxutils
import z3c.table.column
import zope.interface
import zope.schema


class ReviewFields(zope.interface.Interface):

    keep = zope.schema.Choice(title=_(u'Keep imported data?'),
                              source=icemac.addressbook.sources.yes_no_source)


class ImportedTable(icemac.addressbook.browser.table.Table):

    cssClassEven = u'table-even-row'
    cssClassOdd = u'table-odd-row'
    sortOn = None
    no_rows_message = _(u'There was nothing to import in the import file.')

    def setUpColumns(self):
        cols = []
        weight = 0
        for row in icemac.ab.importer.browser.wizard.base.import_mapping:
            fields = zope.schema.getFieldsInOrder(row['interface'])
            first = True
            for field_name, field in fields:
                weight += 1
                if first:
                    header = '<i>%s</i><br />%s' % (
                        row['title'], field.title)
                    first = False
                else:
                    header = '<br />%s' % field.title
                cols.append(self._create_col(
                        row['prefix'], field_name, weight, header))
        return cols

    def renderRow(self, row, cssClass=None):
        rendered_row = super(ImportedTable, self).renderRow(row, cssClass)
        if not row:
            return rendered_row
        return u'\n'.join((rendered_row,
                           self._renderErrors(row[0][0], cssClass)))

    def _create_col(self, prefix, field_name, weight, header):
        "Create a single column according to `prefix` and `field_name`."
        kwargs = {}
        if prefix == 'person':
            column = icemac.addressbook.browser.table.GetAttrColumn
            if field_name == 'keywords':
                column = icemac.addressbook.browser.table.KeywordsGetAttrColumn
        else:
            column = icemac.addressbook.browser.table.AttrGetAttrColumn
            kwargs['masterAttrName'] = 'default_' + prefix
            if field_name in ('country', 'state'):
                column = (
                    icemac.addressbook.browser.table.CountryAttrGetAttrColumn)

        return z3c.table.column.addColumn(
            self, column, field_name, weight=weight, header=header,
            attrName=field_name, **kwargs)

    def _renderErrors(self, item, cssClass):
        errors = self.session['import_errors'][item.__name__]
        result = []
        if errors:
            result.extend([u'<tr class="%s">' % cssClass,
                           u'<td colspan="%s">' % len(self.columns),
                           _(u'Errors:'),
                           u'<ul class="errors">'])
            for error in errors:
                result.append(
                    u'<li>%s</li>' % xml.sax.saxutils.escape(unicode(error)))
            result.extend([u'</ul>',
                           u'</td>',
                           u'</tr>'])
        return u'\n'.join(result)

    @property
    def session(self):
        return icemac.ab.importer.browser.wizard.base.get_file_session(
            self.context, self.request)

    @property
    def values(self):
        addressbook = icemac.addressbook.interfaces.IAddressBook(self.context)
        for id in self.session.get('imported', []):
            yield addressbook[id]


class Review(icemac.ab.importer.browser.wizard.base.FileSessionStorageStep):

    interface = ReviewFields
    label = _(u'Review imported data')

    def renderImportedTable(self):
        table = ImportedTable(self.context, self.request)
        table.update()
        return table.render()

    def render(self):
        result = super(Review, self).render()
        if self.found_errors:
            # make sure data containing errors is not stored
            icemac.ab.importer.browser.wizard.base.delete_imported_data(self)
        return result

    def applyChanges(self, data):
        super(Review, self).applyChanges(data)
        if not data['keep']:
            icemac.ab.importer.browser.wizard.base.delete_imported_data(self)
        return True

    @property
    def found_errors(self):
        """Tells whether there were import errors."""
        return self.getContent().get('found_errors', False)

    @property
    def showNextButton(self):
        """Next button condition."""
        return not self.found_errors
