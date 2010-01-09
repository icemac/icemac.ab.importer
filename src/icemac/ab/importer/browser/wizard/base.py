# -*- coding: utf-8 -*-
# Copyright (c) 2009-2010 Michael Howitz
# See also LICENSE.txt

from icemac.addressbook.i18n import MessageFactory as _
import gocept.cache.property
import icemac.ab.importer.interfaces
import icemac.addressbook.interfaces
import persistent.mapping
import z3c.form.field
import z3c.wizard.wizard
import zope.component
import zope.interface
import zope.security.proxy
import zope.session.interfaces


class ImportWizard(z3c.wizard.wizard.Wizard):

    label = _(u'Import Wizard')

    def setUpSteps(self):
        return [
            z3c.wizard.step.addStep(self, 'editFile', weight=1),
            z3c.wizard.step.addStep(self, 'reader', weight=2),
            z3c.wizard.step.addStep(self, 'map', weight=3),
            z3c.wizard.step.addStep(self, 'review', weight=4),
            z3c.wizard.step.addStep(self, 'complete', weight=5),
            ]


class FileSession(persistent.mapping.PersistentMapping):
    "Session of an import file."

    file = None
    cache = gocept.cache.property.TransactionBoundCache('_cache', dict)


@zope.component.adapter(FileSession)
@zope.interface.implementer(icemac.ab.importer.interfaces.IImportFile)
def file_session_to_import_file(file_session):
    """Get the import file of its session."""
    return file_session.file


def get_file_session(file, request):
    "Get the session associated with the file."
    session = zope.session.interfaces.ISession(request)[
        icemac.addressbook.interfaces.PACKAGE_ID]
    key = 'import_%s' % file.__name__
    file_session = session.get(key, None)
    if file_session is None:
        file_session = FileSession()
        session[key] = file_session
    file_session.file = zope.security.proxy.removeSecurityProxy(file)
    return file_session


class Step(z3c.wizard.step.Step):

    @property
    def fields(self):
        return z3c.form.field.Fields(self.interface)


class FileSessionStorageStep(Step):
    "Step which stores its data in file's session."

    def getContent(self):
        return get_file_session(self.context, self.request)


def get_import_entities():
    "Get the entities relevant for the import."
    name_suffixes = ['person.Person',
                     'address.PostalAddress',
                     'address.PhoneNumber',
                     'address.EMailAddress',
                     'address.HomePageAddress']
    return [zope.component.getUtility(
                icemac.addressbook.interfaces.IEntity,
                name='icemac.addressbook.'+suffix)
            for suffix in name_suffixes]


@zope.interface.implementer(icemac.addressbook.interfaces.IAddressBook)
@zope.component.adapter(icemac.ab.importer.interfaces.IImportFile)
def importfile_to_addressbook(import_file):
    "Adapt import file to address book."
    return import_file.__parent__.__parent__


def delete_imported_data(self):
    """Delete previously imported data."""
    addressbook = icemac.addressbook.interfaces.IAddressBook(self.context)
    session = self.getContent()
    for id in session.get('imported', []):
        try:
            del addressbook[id]
        except KeyError:
            # This can occur when importing the same data again after
            # delting it
            pass
    session['imported'] = []
    keywords = zope.component.getUtility(
        icemac.addressbook.interfaces.IKeywords)
    for id in session.get('imported_keywords', []):
        del keywords[id]
    session['imported_keywords'] = []
