# -*- coding: utf-8 -*-
from decimal import Decimal
from icemac.addressbook.entities import get_bound_schema_field
from icemac.addressbook.interfaces import IEMailAddress
from icemac.addressbook.interfaces import IKeywords, IEntity, IPerson
from icemac.addressbook.interfaces import IPostalAddress, IPhoneNumber
import datetime
import zope.component
import zope.component.hooks


def fields_and_values(person):
    """Get the field names and values of all non-empty person fields.

    The `country` field is omitted.
    """
    def entity_values(iface):
        entity = IEntity(iface)
        for name, field in entity.getRawFields():
            bound = get_bound_schema_field(person, entity, field)
            value = bound.get(bound.context)
            if value and field.title != 'country':
                yield field.title, value
    for iface in (IPerson, IPostalAddress, IPhoneNumber, IEMailAddress):
        for title, value in entity_values(iface):
            yield title, value


def test_map__1(address_book, browser, KeywordFactory, ImportFileFactory):
    """It imports keywords.

    Keywords are comma separated values inside a column. Not yet existing
    keywords get created. Existing ones get used.

    """
    # Create a keyword first to show it gets used:
    KeywordFactory(address_book, u'family')
    ImportFileFactory(address_book, u'keyword.csv', [
        'last_name,xkeywords',
        'Lahn,"family, friends"',
        'Sieg," friends , company"',
        'Pech,'])
    browser.login('mgr')
    browser.open(browser.IMPORTER_FILE_IMPORT_URL)
    browser.getControl('Next').click()
    assert browser.IMPORTER_IMPORT_MAP_URL == browser.url
    browser.getControl('last name').displayValue = [
        'last_name (Lahn, Sieg, Pech)']
    browser.getControl('keywords').displayValue = [
        'xkeywords (family, friends, friends , company)']
    browser.getControl('Next').click()
    assert browser.IMPORTER_IMPORT_REVIEW_URL == browser.url
    assert [
        'Lahn',
        'family, friends',
        'DE',
        'Sieg',
        'company, friends',
        'DE',
        'Pech',
        'DE'] == browser.etree.xpath('//table/tbody/tr/td/text()')
    # The import needs to be completed to view the results:
    browser.getControl('Next').click()
    assert browser.IMPORTER_IMPORT_COMPLETE_URL == browser.url
    browser.getControl('Complete').click()
    assert browser.IMPORTER_OVERVIEW_URL == browser.url
    # The new keywords have been created:
    keywords = zope.component.getUtility(IKeywords, context=address_book)
    assert ([u'company', u'family', u'friends'] ==
            sorted(x.title for x in keywords.get_keywords()))
    # They have been associated to the persons:
    with zope.component.hooks.site(address_book):
        assert ([
            (u'Lahn', [u'family', u'friends']),
            (u'Sieg', [u'company', u'friends']),
            (u'Pech', [])] ==
            [(x.get_name(), sorted(y.title for y in x.keywords))
             for x in address_book.values()])


def test_map__2(
        address_book, browser, some_user_defined_fields, ImportFileFactory):
    """It imports values for user defined fields."""
    # Floating point numbers which are imported into an integer field are
    # floored and converted to an integer number. This is tested in the last
    # two lines of the import file.
    ImportFileFactory(address_book, u'fine.csv', [
        'last_name,foto,meet,states,numbers,costs,mailbox',
        'Utzer,True,2009-10-31 11:31, Sachsen-Anhalt,3,4.3,'
        'I do not like long and boring mail box texts where people tell a '
        'whole story instead of saying: I am not here leave a message.',
        'User,Yes,, Sachsen,6.2,1e3,',
        'Nobody,False,,,5.7,,'])
    browser.login('mgr')
    browser.open(browser.IMPORTER_FILE_IMPORT_URL)
    browser.getControl('Next').click()
    assert browser.IMPORTER_IMPORT_MAP_URL == browser.url
    browser.getControl('last name').displayValue = ['last_name']
    browser.getControl('photo permission?').displayValue = ['foto']
    browser.getControl('last seen').displayValue = ['meet']
    browser.getControl('state').displayValue = ['states']
    browser.getControl('number of letters').displayValue = ['numbers']
    browser.getControl('cost per minute').displayValue = ['costs']
    browser.getControl('mail box text').displayValue = ['mailbox']
    browser.getControl('Next').click()
    assert browser.IMPORTER_IMPORT_REVIEW_URL == browser.url
    # The imported data is shown in the preview, the contents of the `mail
    # box text` column is abbreviated:
    assert [
        'Utzer',
        'True',
        '2009-10-31 11:31:00',
        'DE',
        '3',
        'Sachsen-Anhalt',
        '4.3',
        u'I do not like long and …',
        'User',
        'True',
        'DE',
        '6',
        'Sachsen',
        '1E+3',
        'Nobody',
        'False',
        'DE',
        '5'] == browser.etree.xpath('//table/tbody/tr/td/text()')
    browser.getControl('Next').click()
    assert 'Import complete' in browser.contents
    browser.getControl('Complete').click()
    assert browser.IMPORTER_OVERVIEW_URL == browser.url
    zope.component.hooks.setSite(address_book)
    p1 = address_book['Person']
    assert ([
        (u'last name', u'Utzer'),
        (u'photo permission?', True),
        (u'last seen', datetime.datetime(2009, 10, 31, 11, 31)),
        (u'number of letters', 3),
        (u'state', u'Sachsen-Anhalt'),
        (u'cost per minute', Decimal('4.3')),
        (u'mail box text', u'I do not like long and boring mail box texts '
                           u'where people tell a whole story instead of '
                           u'saying: I am not here leave a message.')
    ] == list(fields_and_values(p1)))
    p2 = address_book['Person-2']
    assert ([
        (u'last name', u'User'),
        (u'photo permission?', True),
        (u'number of letters', 6),
        (u'state', u'Sachsen'),
        (u'cost per minute', Decimal('1E+3'))
    ] == list(fields_and_values(p2)))
    p3 = address_book['Person-3']
    assert ([
        (u'last name', u'Nobody'),
        (u'number of letters', 5)
    ] == list(fields_and_values(p3)))


def test_map__3(address_book, browser, ImportFileFactory):
    """There was a bug which occurred when doing the following steps:

    * importing persons
    * deleting all persons
    * importing the same import file as in the first step

    """
    ImportFileFactory(address_book, u'del.csv', ["last_name", "Vipraschil"])
    browser.login('mgr')
    browser.open(browser.IMPORTER_FILE_IMPORT_URL)
    browser.getControl('Next').click()
    assert browser.IMPORTER_IMPORT_MAP_URL == browser.url
    browser.getControl('last name').displayValue = ['last_name']
    browser.getControl('Next').click()
    assert browser.IMPORTER_IMPORT_REVIEW_URL == browser.url
    browser.getControl('Next').click()
    assert browser.IMPORTER_IMPORT_COMPLETE_URL == browser.url
    browser.getControl('Complete').click()
    assert browser.IMPORTER_OVERVIEW_URL == browser.url
    # Delete all persons in address book
    browser.open(browser.ADDRESS_BOOK_EDIT_URL)
    browser.getControl('Delete all persons in address book').click()
    assert browser.ADDRESS_BOOK_DELETE_PERSONS_URL == browser.url
    browser.getControl('Yes').click()
    assert 'Address book contents deleted.' == browser.message
    # When importing the same import file, previously an error occurred:
    browser.open(browser.IMPORTER_FILE_IMPORT_URL)
    browser.getControl('Next').click()
    assert browser.IMPORTER_IMPORT_MAP_URL == browser.url
    assert (['Current step:', 'Map fields'] ==
            browser.etree.xpath('//div[@class="currStep"]/span/text()'))
