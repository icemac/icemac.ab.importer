from __future__ import unicode_literals


def test_edit__EditFile__1(
        address_book, browser, import_file, ImportFileFactory):
    """It allows to replace the import file."""
    ImportFileFactory(address_book, '1.csv', 'last_name')
    browser.login('mgr')
    browser.open(browser.IMPORTER_FILE_IMPORT_URL)
    browser.getControl('Back').click()
    assert browser.IMPORTER_IMPORT_EDIT_URL == browser.url
    browser.getControl('file', index=1).add_file(
        import_file('first_name'), 'text/plain', 'header.csv')
    browser.getControl('Next').click()
    assert browser.IMPORTER_IMPORT_READER_URL == browser.url
    # The original file was really replaced:
    browser.getControl('Back').click()
    assert browser.IMPORTER_IMPORT_EDIT_URL == browser.url
    assert 'header.csv' == browser.getControl('name').value
    browser.getLink('Download file').click()
    assert 'first_name' == browser.contents
