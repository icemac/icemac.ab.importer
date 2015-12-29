# -*- coding: utf-8 -*-
from StringIO import StringIO
from icemac.addressbook.interfaces import IKeywords
from mock import patch
import gocept.country.db
import pytest
import zope.component


@pytest.fixture('function')
def example_data():
    """Construct an import file which contains errors for these constraints:

     - last name of the person must not be empty

      - birth date column must be empty or contain a valid date

      - e-mail address must be valid

      - home page address must be a URI

      - country must be either the ISO country code or the country name

      - data line must contain enough fields

    Not each field must be selected when mapping the fields. (The Field `asdf`
    is used as an example here.)

    """
    file_data = StringIO()
    file_data.write('\n'.join([
        'last_name,birth_date,e_mail_addr,www,asdf,countries,pnotes',
        ',1999-09-09,,,asdf,,',  # missing last name
        '"wrong date",1981,,,,,,',
        '"wrong e-mail",,i@me@de,,,,',
        '"wrong home page address",,i@me.de,asdf,,,',
        '"wrong country",,,,,D,',
        '"country ISO code",,,,,AT,',
        '"not enough fields",,',
        '" nice "," 2006-06-06", r6@ab.info," http://www.r6.sf.net",,'
        '" Switzerland ",'
        '"  my r e a l l y   long, but also really nice  notes    "']))
    file_data.seek(0)
    return file_data


def test_review__ImportedTable__renderRow__1(
        address_book, browser, example_data):
    """It renders error messages if data does not match the constraints.

    There are a number of constraints the imported data must fulfill
    otherwise error messages are displayed. Most constraints are tested here
    together.

    White spaces at beginning and end are striped. When a notes field
    contains more then 20 characters it get nicely truncated. (See line
    with `last_name` ``nice`` for both cases.)

    """
    browser.login('mgr')
    browser.open(browser.IMPORTER_FILE_ADD_URL)
    # Upload the example file:
    browser.getControl('file').add_file(
        example_data, 'text/plain', 'errors.csv')
    browser.getControl('Add').click()
    assert '"errors.csv" added.' == browser.message
    browser.getLink('Import', index=0).click()
    assert browser.IMPORTER_FILE_IMPORT_URL == browser.url
    # Map the fields:
    browser.getControl('Next').click()
    assert browser.IMPORTER_IMPORT_MAP_URL == browser.url
    browser.getControl('last name').displayValue = [
        'last_name (wrong date, wrong e-mail)']
    browser.getControl('birth date').displayValue = [
        'birth_date (1999-09-09, 1981)']
    browser.getControl('notes', index=0).displayValue = ['pnotes']
    browser.getControl('e-mail address').displayValue = [
        'e_mail_addr (i@me@de)']
    browser.getControl('country').displayValue = ['countries']
    browser.getControl('URL').displayValue = ['www']
    with patch('gocept.country.CountrySource.getValues') as getValues:
        getValues.return_value = [
            gocept.country.db.Country('AF'),
            gocept.country.db.Country('AT'),
            gocept.country.db.Country('CH'),
            gocept.country.db.Country('DE'),
        ]
        browser.getControl('Next').click()
    # The review step shows the error messages:
    assert browser.IMPORTER_IMPORT_REVIEW_URL == browser.url
    assert [
        'person -- last name: Required input is missing.',
        'person -- birth date: 1981 is no valid date.',
        'e-mail address -- e-mail address: i@me@de is not a valid e-mail '
        'address.',
        'home page address -- URL: The specified URI is not valid.',
        'postal address -- country: Value D is not allowed. Allowed values '
        'are: AF, AT, CH, DE',
        'home page address: Not enough data fields in row.',
        'person: Not enough data fields in row.',
        'postal address: Not enough data fields in row.',
    ] == browser.etree.xpath('//ul[@class="errors"]/li/text()')
    # As there are errors, there is no `next` button:
    assert ['form.buttons.back'] == browser.submit_control_names
    # Selecting the `back` button shows that the selected mapping has been
    # kept:
    browser.getControl('Back').click()
    assert (['last_name (wrong date, wrong e-mail)'] ==
            browser.getControl('last name').displayValue)
    assert (['birth_date (1999-09-09, 1981)'] ==
            browser.getControl('birth date').displayValue)
    assert (['pnotes'] == browser.getControl('notes', index=0).displayValue)
    assert (['e_mail_addr (i@me@de)'] ==
            browser.getControl('e-mail address').displayValue)
    assert (['countries'] == browser.getControl('country').displayValue)
    assert (['www'] == browser.getControl('URL').displayValue)
    browser.getControl('Next').click()
    # As the user can't go further from the review step he could upload another
    # import file or abort the import right now by selecting any link outside
    # the importer. None of the data rows got imported as there were errors:
    browser.open(browser.PERSONS_LIST_URL)
    assert 'There are no persons entered yet' in browser.contents


def test_review__ImportedTable__renderRow__2(
        address_book, browser, some_user_defined_fields, ImportFileFactory):
    """It renders errors if content for user defined fields is invalid."""
    ImportFileFactory(address_book, u'fail.csv', [
        'last_name,foto,meet,states,numbers,costs,mailbox',
        'wrong bool,2009-10-31,,,,,',
        'wrong bool 2,asdf,,,,,',
        'wrong datetime,,2.2.2002 13.24,,,,',
        'wrong statename,,,Berlin,,,',
        'wrong int,,,,asd,,',
        'wrong decimal,,,,,qwe,'])
    browser.login('mgr')
    browser.open(browser.IMPORTER_FILE_IMPORT_URL)
    browser.getControl('Next').click()
    assert browser.IMPORTER_IMPORT_MAP_URL == browser.url
    browser.getControl('last name').displayValue = [
        'last_name (wrong bool, wrong bool 2, wrong datetime)']
    browser.getControl('photo permission?').displayValue = [
        'foto (2009-10-31, asdf)']
    browser.getControl('last seen').displayValue = ['meet (2.2.2002 13.24)']
    browser.getControl('state').displayValue = ['states']
    browser.getControl('number of letters').displayValue = ['numbers']
    browser.getControl('cost per minute').displayValue = ['costs']
    browser.getControl('mail box text').displayValue = ['mailbox']
    browser.getControl('Next').click()
    assert browser.IMPORTER_IMPORT_REVIEW_URL == browser.url
    assert [
        'person -- photo permission?: Value 2009-10-31 is not allowed. '
        'Allowed values are: yes, true, no, false',
        'person -- photo permission?: Value asdf is not allowed. '
        'Allowed values are: yes, true, no, false',
        'person -- last seen: 2.2.2002 13.24 is no valid datetime. '
        'Must match to format string "%Y-%m-%d %H:%M".',
        'postal address -- state: Value Berlin is not allowed. '
        'Allowed values are: Sachsen, Sachsen-Anhalt, Brandenburg',
        'postal address -- number of letters: asd is not a valid integer '
        'number.',
        'phone number -- cost per minute: qwe is not a valid decimal number.',
    ] == browser.etree.xpath('//ul[@class="errors"]/li/text()')


def test_review__ImportedTable__renderTable__1(
        address_book, browser, ImportFileFactory):
    """It renders an error message if there is nothing to import."""
    ImportFileFactory(address_book, u'header.csv', ['last_name'])
    browser.login('mgr')
    browser.open(browser.IMPORTER_FILE_IMPORT_URL)
    browser.getControl('Next').click()
    assert browser.IMPORTER_IMPORT_MAP_URL == browser.url
    browser.getControl('last name').displayValue = ['last_name']
    browser.getControl('Next').click()
    # On the review step a message tells that there is nothing to import:
    assert browser.IMPORTER_IMPORT_REVIEW_URL == browser.url
    assert 'There was nothing to import in the import file' in browser.contents
    # It is possible to go to the complete step as there are no errors:
    browser.getControl('Next').click()
    assert browser.IMPORTER_IMPORT_COMPLETE_URL == browser.url
    browser.getControl('Complete').click()
    assert browser.IMPORTER_OVERVIEW_URL == browser.url


def test_review__Review__applyChanges__1(
        address_book, browser, ImportFileFactory, KeywordFactory):
    """It allows to discard the imported data.

    Newly created keywords get also deleted, but existing ones are kept.
    """
    KeywordFactory(address_book, u'family')
    ImportFileFactory(address_book, u'abc.csv', [
        'last_name,xkeywords',
        'Abc,"ccc, company"'])
    browser.login('mgr')
    browser.open(browser.IMPORTER_FILE_IMPORT_URL)
    browser.getControl('Next').click()
    assert browser.IMPORTER_IMPORT_MAP_URL == browser.url
    browser.getControl('last name').displayValue = ['last_name (Abc)']
    browser.getControl('keywords').displayValue = ['xkeywords (ccc, company)']
    browser.getControl('Next').click()
    # The review step shows the result and allows to discard the imported data:
    assert browser.IMPORTER_IMPORT_REVIEW_URL == browser.url
    assert (['Abc', 'ccc, company', 'DE'] ==
            browser.etree.xpath('//table/tbody/tr/td/text()'))
    browser.getControl('Keep imported data?').displayValue = ['no']
    # Completing the import deletes the imported data and keywords:
    browser.getControl('Next').click()
    assert browser.IMPORTER_IMPORT_COMPLETE_URL == browser.url
    browser.getControl('Complete').click()
    assert browser.IMPORTER_OVERVIEW_URL == browser.url
    # No new keywords have been created:
    keywords = zope.component.getUtility(IKeywords, context=address_book)
    assert [u'family'] == sorted(x.title for x in keywords.get_keywords())
    # No new persons have been created:
    assert [] == list(address_book)

# delete ../keywords.txt
