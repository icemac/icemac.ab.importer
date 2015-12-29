def test_wizard__end_to_end__1(address_book, browser, ImportFileFactory):
    """It allows to import data from a file into the address book."""
    ImportFileFactory(address_book, u'first.csv', [
        "firstname,last_name,addr_city",
        "Rene Manfred,Kohn,Hiernase",
        "Jurgen,Krafft,Dortmund"])
    browser.login('mgr')
    browser.open(browser.IMPORTER_FILE_IMPORT_URL)
    # The first step is to choose a reader for the import file. Only the
    # readers capable to import the file are displayed:

    assert (['CSV file (comma separated fields, ISO-dates, UTF-8 encoded)'] ==
            browser.getControl('Import file reader').displayOptions)
    browser.getControl('Next').click()
    assert browser.IMPORTER_IMPORT_MAP_URL == browser.url
    # For each field in the address book the corresponding field in the import
    # file can be chosen. Not only the names of the fields in the import file
    # are shown but also some sample values:
    assert [
        'No value',
        'firstname (Rene Manfred, Jurgen)',
        'last_name (Kohn, Krafft)',
        'addr_city (Hiernase, Dortmund)'
    ] == browser.getControl('first name').displayOptions
    browser.getControl('first name').displayValue = ['firstname']
    browser.getControl('last name').displayValue = ['last_name']
    browser.getControl('city').displayValue = ['addr_city']
    browser.getControl('Next').click()
    assert browser.IMPORTER_IMPORT_REVIEW_URL == browser.url
    # In the next step the imported data is displayed as it was stored in the
    # address book.
    assert [
        'Rene Manfred',
        'Kohn',
        'Hiernase',
        'DE',
        'Jurgen',
        'Krafft',
        'Dortmund',
        'DE'] == browser.etree.xpath('//table/tbody/tr/td/text()')
    # The user can decide to keep the values:
    assert ['yes'] == browser.getControl('Keep imported data?').displayValue
    browser.getControl('Next').click()
    assert browser.IMPORTER_IMPORT_COMPLETE_URL == browser.url
    # The last step tells that the import is complete. The `complete` button
    # leads back to the list of import files:
    assert 'Import complete.' in browser.contents
    browser.getControl('Complete').click()
    assert browser.IMPORTER_OVERVIEW_URL == browser.url
    # The import file is still displayed:
    assert ['first.csv',
            'Delete', 'Import'] == browser.etree.xpath('//td/a/text()')
    # The imported persons are displayed on the person list:
    browser.open(browser.PERSONS_LIST_URL)
    assert ['Kohn', 'Rene Manfred',
            'Krafft', 'Jurgen'] == browser.etree.xpath('//td/a/text()')
