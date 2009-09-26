# -*- coding: utf-8 -*-
# Copyright (c) 2009 Michael Howitz
# See also LICENSE.txt

from icemac.addressbook.i18n import MessageFactory as _
import gocept.reference.field
import icemac.ab.importer.browser.wizard.base
import icemac.ab.importer.interfaces
import icemac.addressbook.interfaces
import persistent.mapping
import z3c.form.field
import zc.sourcefactory.contextual
import zope.component
import zope.event
import zope.interface
import zope.schema
import zope.security.proxy
import zope.site.hooks


NONE_REPLACEMENT = object()


def get_reader(session):
    if not hasattr(session, 'cache'):
        # we are in a dict below the session (storing field group
        # data), so we have to use the "uplink"
        session = session['__parent__']
    reader = session.cache.get('reader', None)
    if reader is not None:
        return reader
    reader_name = session['reader']
    reader = zope.component.getAdapter(
        None,
        icemac.ab.importer.interfaces.IImportFileReader,
        name=reader_name)
    file = zope.security.proxy.removeSecurityProxy(session.file.openDetached())
    reader = reader.open(file)
    session.cache['reader'] = reader
    return reader


class ImportFields(zc.sourcefactory.contextual.BasicContextualSourceFactory):
    "Where to put the imported data in the addressbook."

    def getValues(self, context):
        return xrange(len(list(get_reader(context).getFieldNames())))

    def getTitle(self, context, value):
        reader = get_reader(context)
        field_name = list(reader.getFieldNames())[value]
        samples = u', '.join(
            x for x in reader.getFieldSamples(field_name) if x)
        title = field_name
        if samples:
            title = '%s (%s)' % (field_name, samples)
        return title

import_fields = ImportFields()

def split_keywords(keywords):
    return [x.strip() for x in keywords.split(',')]

class IFieldValue(zope.interface.Interface):
    "Value for a specific field."

    def __call__():
        "Return the value."


# field value converters
@zope.component.adapter(None, None)
@zope.interface.implementer(IFieldValue)
def unchanged_field(value, field):
    if value is None:
        # We can't return None, as this means that the adapter can't adapt.
        return NONE_REPLACEMENT
    return value


@zope.interface.implementer(IFieldValue)
def text_field(value, field):
    "Adapter for `Text`, `TextLine` and `Choice` fields."
    if value is None:
        # We can't return None, as this means that the adapter can't adapt.
        return NONE_REPLACEMENT
    return value.strip()


@zope.component.adapter(None, zope.schema.interfaces.IURI)
@zope.interface.implementer(IFieldValue)
def uri_field(value, field):
    if value is None:
        # We can't return None, as this means that the adapter can't adapt.
        return NONE_REPLACEMENT
    return value.strip().encode('ascii')


@zope.component.adapter(None, zope.schema.interfaces.IChoice)
@zope.interface.implementer(IFieldValue)
def country_or_state_field(value, field):
    if value is None:
        # We can't return None, as this means that the adapter can't adapt.
        return NONE_REPLACEMENT
    value = value.strip()
    for candidate in field.source.factory.getValues():
        if candidate.token == value:
            return candidate
        if field.source.factory.getTitle(candidate) == value:
            return candidate
    # value not found in source --> can't adapt
    return None


@zope.component.adapter(None, gocept.reference.field.Set)
@zope.interface.implementer(IFieldValue)
def keywords_field(value, field):
    keywords = set()
    if value is None:
        return keywords
    keyword_util = zope.component.getUtility(
        icemac.addressbook.interfaces.IKeywords)
    for keyword_title in split_keywords(value):
        keywords.add(keyword_util.get_keyword_by_title(keyword_title))
    return keywords


class IErrorMessage(zope.interface.Interface):
    """Render import error message."""

    def __unicode__():
        """Return error text."""


# Error renderers
@zope.interface.implementer(IErrorMessage)
def simple_invalid(field, exc):
    return exc.doc()


@zope.component.adapter(zope.schema.interfaces.IChoice,
                        zope.schema.interfaces.ConstraintNotSatisfied)
@zope.interface.implementer(IErrorMessage)
def choice_constraint_not_satisfield(field, exc):
    value = exc.args[0]
    return _(u'Value %s not allowed. Allowed values: %s') % (
        value, ', '.join(str(x) for x in field.source.factory.getValues()))


@zope.component.adapter(zope.schema.interfaces.IChoice,
                        zope.schema.interfaces.ConstraintNotSatisfied)
@zope.interface.implementer(IErrorMessage)
def country_or_state_constraint_not_satisfield(field, exc):
    value = exc.args[0]
    titles = [_(u'%s resp. %s') % (x.token, field.source.factory.getTitle(x))
              for x in field.source.factory.getValues()]
    return _(u'Value %s not allowed. Allowed values: %s') % (
        value, ', '.join(titles))


@zope.component.adapter(zope.schema.interfaces.IDate,
                        zope.schema.interfaces.WrongType)
@zope.interface.implementer(IErrorMessage)
def date_wrong_type(field, exc):
    value = exc.args[0]
    return _(u'%s is no valid date.') % value


@zope.component.adapter(None, zope.schema.interfaces.ConstraintNotSatisfied)
@zope.interface.implementer(IErrorMessage)
def email_constraint_not_satisfield(field, exc):
    value = exc.args[0]
    return _(u'%s is not a valid e-mail address.') % value


@zope.component.adapter(None, IndexError)
@zope.interface.implementer(IErrorMessage)
def index_error(field, exc):
    return _(u'Not enough data fields in row.')


def render_error(interface, field_name, exc):
    "Render the error text using the error render adapters."
    obj_title = icemac.ab.importer.browser.wizard.base.\
        getImportMappingRowForInterface(interface)['title']

    if field_name is None:
        field = ''
        title = obj_title
        # need to set the field name to the default here, as
        # queryMultiAdapter call with name=None behaves strange, it
        # seems to delete all adapters matching objects and interface.
        field_name = u''
    else:
        field = interface[field_name]
        title = '%s - %s' % (obj_title, field.title)

    # try named adapter first
    message = zope.component.queryMultiAdapter(
        (field, exc), IErrorMessage, name=field_name)
    if message is None:
        # fallback to default (unnamed) adapter
        message = zope.component.getMultiAdapter(
            (field, exc), IErrorMessage)

    return u'%s: %s' % (title, message)

class KeywordBuilder(object):

    KEYWORD_FIELD_NAME = "person-0.keywords"
    keyword_index = None
    keywords = None

    def __init__(self, user_data):
        """Expects a mapping between name of the field in the address book and
        field index in import file.

        Example: person-0.first_name --> 0
                 home_page_address-2.notes --> 11
        """
        if self.KEYWORD_FIELD_NAME in user_data:
            self.keyword_index = user_data[self.KEYWORD_FIELD_NAME]
            self.keywords = zope.component.getUtility(
                icemac.addressbook.interfaces.IKeywords)

    def create(self, data):
        created = []
        if self.keyword_index is None:
            return created
        keyword_data = data[self.keyword_index]
        if keyword_data is None:
            return created
        for keyword_title in split_keywords(keyword_data):
            if self.keywords.get_keyword_by_title(keyword_title, None) is None:
                keyword = icemac.addressbook.utils.create_obj(
                    icemac.addressbook.keyword.Keyword, keyword_title)
                icemac.addressbook.utils.add(self.keywords, keyword)
                created.append(keyword)
        return created


class ImportObjectBuilder(object):
    """Build the objects the user wants to import."""

    def __init__(self, user_data, address_book, entries_number):
        """Expects a mapping between name of the field in the address book and
        field index in import file and
        .

        Example: person-0.first_name --> 0
                 home_page_address-3.notes --> 11

        Stores the address book field names in dictionaries on
        attributes mapping to the index in the import file.

        address_book ... address book to create the objects in.
        entries_number ... number of entries of each address kind.

        """
        self.address_book = address_book
        self.entries_number = entries_number
        for row in icemac.ab.importer.browser.wizard.base.import_mapping:
            for index in xrange(self.entries_number):
                setattr(self, "%s-%s" % (row['prefix'], index), {})
        for field_desc, index in user_data.iteritems():
            if index is None:
                continue # field was not selected for import
            prefix, field_name = field_desc.split('.')
            getattr(self, prefix)[field_name] = index

    def create(self, data):
        """Create an object for data.

        data ... import data row, mapping between field index and value."""
        self.errors = set()
        person = self._create('person-0', self.address_book, data)
        self._validate(
            icemac.ab.importer.browser.wizard.base.person_mapping['interface'],
            person)
        for address in icemac.addressbook.address.address_mapping:
            for index in xrange(self.entries_number):
                prefix = "%s-%s" % (address['prefix'], index)
                obj = self._create(prefix, person, data)
                if index == 0:
                    # set the created address as default address of its kind
                    setattr(person, 'default_'+address['prefix'], obj)
                self._validate(address['interface'], obj)
        return person, sorted(list(self.errors))

    def _create(self, prefix, parent, data):
        # map address book field name to value
        row_prefix, row_index = prefix.split('-')
        row = (
            icemac.ab.importer.browser.wizard.base.
            getImportMappingRowForPrefix(row_prefix))
        obj = icemac.addressbook.utils.create_obj(row['class_'])

        iface = row['interface']
        for field_name, index in getattr(self, prefix).iteritems():
            # get, convert and set values
            field = iface[field_name]
            try:
                value = data[index]
            except IndexError, e:
                self.errors.add(render_error(iface, None, e))
            else:
                # try named converter first
                conv_value = zope.component.queryMultiAdapter(
                    (value, field), IFieldValue, name=field_name)
                if conv_value is None:
                    # fallback to default (unnamed) converter
                    conv_value = zope.component.getMultiAdapter(
                        (value, field), IFieldValue)
                if conv_value is NONE_REPLACEMENT:
                    conv_value = None
                try:
                    field.set(obj, conv_value)
                except zope.interface.Invalid, e:
                    self.errors.add(render_error(iface, field_name, e))

        icemac.addressbook.utils.add(parent, obj)
        return obj

    def _validate(self, interface, obj):
        for field_name, exc in zope.schema.getValidationErrors(interface, obj):
            self.errors.add(render_error(interface, field_name, exc))


class FieldsGroup(z3c.form.group.Group):
    "Fields grouped by object."

    def __init__(self, context, request, parent, interface, label, prefix):
        super(FieldsGroup, self).__init__(context, request, parent)
        self.label = label
        self.prefix = prefix
        fields = []
        for field_name in zope.schema.getFieldNamesInOrder(interface):
            field = interface[field_name]
            choice = zope.schema.Choice(
                title=field.title, description=field.description,
                required=False, source=import_fields)
            choice.__name__ = field_name
            fields.append(choice)
        self.fields = z3c.form.field.Fields(*fields, **dict(prefix=prefix))

    def getContent(self):
        if self.prefix not in self.context:
            self.context[self.prefix] = persistent.mapping.PersistentMapping()
            # We need to store the parent here to find the way back to
            # the parent in `get_reader`.
            self.context[self.prefix]['__parent__'] = self.context
        return self.context[self.prefix]


class MapFields(z3c.form.group.GroupForm,
                icemac.ab.importer.browser.wizard.base.FileSessionStorageStep):
    "Map the fields in the import file to fields in the addressbook."

    label = _(u'Map fields')

    def __init__(self, *args, **kw):
        super(MapFields, self).__init__(*args, **kw)
        session = self.getContent()
        request = self.request
        self.groups = []
        for row in icemac.ab.importer.browser.wizard.base.import_mapping:
            if row['prefix'] == 'person':
                entries_number = 1
                main_prefix = ''
            else:
                entries_number = session.get('entries_number', 0)
                main_prefix = _(u'main')
            for index in xrange(entries_number):
                if index == 0:
                    row_title_prefix = main_prefix
                else:
                    row_title_prefix = _(u'other')
                title = row_title_prefix + ' ' + row['title']
                prefix = '%s-%s' % (row['prefix'], index)
                self.groups.append(
                    FieldsGroup(session, request, self, row['interface'],
                                title, prefix))

    @property
    def fields(self):
        return z3c.form.field.Fields()

    def update(self):
        super(MapFields, self).update()
        icemac.ab.importer.browser.wizard.base.FileSessionStorageStep.update(
            self)
        if not self.nextURL:
            # no redirect to next step, make sure no imported data exists
            icemac.ab.importer.browser.wizard.base.delete_imported_data(self)

    def applyChanges(self, data):
        super(MapFields, self).applyChanges(data)
        import_object_builder = ImportObjectBuilder(
            data, icemac.addressbook.interfaces.IAddressBook(self.context),
            self.getContent()['entries_number'])
        keyword_builder = KeywordBuilder(data)
        session = self.getContent()
        reader = get_reader(session)
        imported = session['imported'] = []
        imported_keywords = session['imported_keywords'] = []
        import_errors = session['import_errors'] = {}
        session['found_errors'] = False
        for data_row in reader:
            imported_keywords.extend(x.__name__
                                     for x in keyword_builder.create(data_row))
            obj, errors = import_object_builder.create(data_row)
            imported.append(obj.__name__)
            import_errors[obj.__name__] = errors
            if errors:
                session['found_errors'] = True
