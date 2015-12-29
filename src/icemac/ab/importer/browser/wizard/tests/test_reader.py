from icemac.addressbook.interfaces import IPhoneNumber
import zope.component.hooks


def test_reader__ReaderSettings__1(address_book, browser, ImportFileFactory):
    """It has an empty import file readers list on empty import file."""
    ImportFileFactory(address_book, u'empty.csv', [''])
    browser.login('mgr')
    browser.open(browser.IMPORTER_FILE_IMPORT_URL)
    # There is no import file reader, as the CSV reader expects a first line
    # containing the field names:
    assert [] == browser.getControl('Import file reader').displayOptions


def test_reader__ReaderSettings__2(address_book, browser, ImportFileFactory):
    """It allows to import multiple addresses and numbers."""
    ImportFileFactory(address_book, u'multi.csv', [
        'last_name,1st_phone,2nd_phone,3rd_phone',
        'One,112,110,108',
        'Two,,116116,',
        'Three,1111,,2222',
        'Four,,,'])
    browser.login('mgr')
    browser.open(browser.IMPORTER_FILE_IMPORT_URL)
    assert (
        '1' ==
        browser.getControl('Number of e.g. phone numbers per person').value)
    browser.getControl('Number of e.g. phone numbers per person').value = '3'
    browser.getControl('Next').click()
    assert browser.IMPORTER_IMPORT_MAP_URL == browser.url
    browser.getControl('last name').displayValue = [
        'last_name (One, Two, Three)']
    browser.getControl('number', index=0).displayValue = [
        '1st_phone (112, 1111)']
    browser.getControl('number', index=1).displayValue = [
        '2nd_phone (110, 116116)']
    browser.getControl('number', index=2).displayValue = [
        '3rd_phone (108, 2222)']
    browser.getControl('Next').click()
    # The review step shows the import result, the first phone number is the
    # default one:
    assert browser.IMPORTER_IMPORT_REVIEW_URL == browser.url
    assert [
        'first name',
        'last name',
        'birth date',
        'keywords',
        'notes',
        'address prefix',
        'street',
        'city',
        'zip',
        'country',
        'address prefix',
        'street',
        'city',
        'zip',
        'country',
        'address prefix',
        'street',
        'city',
        'zip',
        'country',
        'number',
        'number',
        'number',
        'e-mail address',
        'e-mail address',
        'e-mail address',
        'URL',
        'URL',
        'URL',
        'One',
        'DE',
        '112',
        '110',
        '108',
        'Two',
        'DE',
        '116116',
        'Three',
        'DE',
        '1111',
        '2222',
        'Four',
        'DE'] == browser.etree.xpath('//th/text() | //td//text()')
    # After completing the import the imported data can be inspected:
    browser.getControl('Next').click()
    assert browser.IMPORTER_IMPORT_COMPLETE_URL == browser.url
    browser.getControl('Complete').click()
    assert browser.IMPORTER_OVERVIEW_URL == browser.url
    zope.component.hooks.setSite(address_book)
    # The first phone number is the main one and it is displayed as the main
    # phone number in the form below, too:
    p1 = address_book['Person']
    assert u'One' == p1.get_name()
    assert '112' == p1.default_phone_number.number
    assert (['112', '110', '108'] ==
            [x.number for x in p1.values() if IPhoneNumber.providedBy(x)])
    # When there is no first one an empty main number is created:
    p2 = address_book['Person-2']
    assert u'Two' == p2.get_name()
    assert None is p2.default_phone_number.number
    assert ([None, '116116'] ==
            [x.number for x in p2.values() if IPhoneNumber.providedBy(x)])
    # Empty non-main phone numbers are not created, so the missing 2nd number
    # is left out and the third one gets the one and only non-main phone
    # number:
    p3 = address_book['Person-3']
    assert u'Three' == p3.get_name()
    assert '1111' == p3.default_phone_number.number
    assert (['1111', '2222'] ==
            [x.number for x in p3.values() if IPhoneNumber.providedBy(x)])
    # But there must be a default number which is always created:
    p4 = address_book['Person-4']
    assert u'Four' == p4.get_name()
    assert None is p4.default_phone_number.number
    assert ([None] ==
            [x.number for x in p4.values() if IPhoneNumber.providedBy(x)])

# delete ../multientries.txt
