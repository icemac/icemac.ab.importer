# -*- coding: utf-8 -*-
# Copyright (c) 2009-2010 Michael Howitz
# See also LICENSE.txt

from icemac.addressbook.i18n import MessageFactory as _
import icemac.addressbook.browser.table
import icemac.addressbook.interfaces
import icemac.addressbook.sources
import xml.sax.saxutils
import z3c.table.column
import zope.i18n
import zope.interface
import zope.schema
import zope.security.proxy


class ContainerColumn(z3c.table.column.GetAttrColumn):
    "Context is a container, search values in container items."
    interface = None # search only objects providing this interface
    container_interface = None # when value provides this interface, lookup
                               # atribute on container
    index = 0 # index in the list of found objects
    attrName = None # attr to look up
    attrInterface = None # interface of the attribute (needed to look up user
                         # defined fields)

    def getObject(self, container):
        if (self.container_interface and
            self.container_interface == self.interface):
            return container
        candidates = list(icemac.addressbook.utils.iter_by_interface(
                container, self.interface))
        if self.index < len(candidates):
            return candidates[self.index]
        return None

    def getRawValue(self, item):
        # user fields are stored in annotation which are not
        # accessible with security proxy. This is no security hole
        # here as only administators may access the importer.
        obj = zope.security.proxy.getObject(self.getObject(item))
        if obj is not None:
            obj = self.attrInterface(obj)
        return self.getValue(obj)

    def getRenderedValue(self, item):
        value = self.getRawValue(item)
        if value is None:
            value = u''
        return value

    def renderCell(self, item):
        return self.getRenderedValue(item)


class CountryColumn(ContainerColumn):
    """ContainerColumn for gocept.country objects."""

    def getRawValue(self, obj):
        country = super(CountryColumn, self).getRawValue(obj)
        if country:
            country = country.token
        return country


class TruncatedContentColumn(ContainerColumn):

    length = 20
    ellipsis = u'…'

    def getRawValue(self, obj):
        value = super(TruncatedContentColumn, self).getRawValue(obj)
        return icemac.truncatetext.truncate(value, self.length, self.ellipsis)


class KeywordsColumn(z3c.table.column.GetAttrColumn):
    """GetAttrColumn where attr is an iterable of keywords."""

    def getValue(self, obj):
        values = super(KeywordsColumn, self).getValue(obj)
        return u', '.join(
            icemac.addressbook.interfaces.ITitle(x) for x in values)


def columnFactory(column):
    """Create a factory which returns the column, so the column can be used as
    an adapter without instanciating it."""
    def factory(context, field):
        return column
    return factory


ContainerColumnFactory = columnFactory(ContainerColumn)
CountryColumnFactory = columnFactory(CountryColumn)
TruncatedContentColumnFactory = columnFactory(TruncatedContentColumn)
KeywordsColumnFactory = columnFactory(KeywordsColumn)


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
        import_entities = (
            icemac.ab.importer.browser.wizard.base.get_import_entities())
        for entity in import_entities:
            if entity.class_name == 'icemac.addressbook.person.Person':
                entries_number = 1
                main_prefix = ''
            else:
               entries_number = self.session['entries_number']
               main_prefix = _(u'main')
            for index in xrange(entries_number):
                first = True
                for field_name, field in entity.getFieldsInOrder():
                    weight += 1
                    if first:
                        if index == 0:
                            title_prefix = main_prefix
                        else:
                            title_prefix = _(u'other')
                        title = _('${prefix} ${title}',
                                  mapping=dict(prefix=title_prefix,
                                               title=entity.title))
                        header = _(
                            '<i>${prefix}</i><br />${title}',
                            mapping=dict(prefix=title, title=field.title))
                        first = False
                    else:
                        header = _('<br />${title}',
                                   mapping=dict(title=field.title))
                    cols.append(self._create_col(
                        entity, field, field_name, weight, header, index))
        return cols

    def renderRow(self, row, cssClass=None):
        rendered_row = super(ImportedTable, self).renderRow(row, cssClass)
        if not row:
            return rendered_row
        return u'\n'.join((rendered_row,
                           self._renderErrors(row[0][0], cssClass)))

    def _create_col(self, entity, field, field_name, weight, header, index):
        "Create a single column for the field."
        # try named adapter first
        column = zope.component.queryMultiAdapter(
            (self.context, field), z3c.table.interfaces.IColumn,
            name=field_name)
        if column is None:
            # the default adapter needs to exist
            column = zope.component.getMultiAdapter(
                (self.context, field), z3c.table.interfaces.IColumn)

        return z3c.table.column.addColumn(
            self, column, field_name, weight=weight, header=header,
            container_interface=icemac.addressbook.interfaces.IPerson,
            interface=entity.interface, attrInterface=field.interface,
            attrName=field_name, index=index)

    def _renderErrors(self, item, cssClass):
        errors = self.session['import_errors'][item.__name__]
        result = []
        if errors:
            result.extend([u'<tr class="%s">' % cssClass,
                           u'<td colspan="%s">' % len(self.columns),
                           zope.i18n.translate(_(u'Errors:'),
                                               context=self.request),
                           u'<ul class="errors">'])
            for error in errors:
                result.append(
                    u'<li>%s</li>' % xml.sax.saxutils.escape(unicode(
                        zope.i18n.translate(error, context=self.request))))
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
