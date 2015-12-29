from icemac.ab.importer.interfaces import IImportFile
from mechanize import HTTPError
import pytest

# Fixtures


@pytest.fixture('function')
def importer_link(browser):
    """Generate the importer link rendered on the master data view."""
    return '<a href="{}"><span>Import data</span></a>'.format(
        browser.IMPORTER_OVERVIEW_URL)


# Tests


def test_importer__CRUD__1(address_book, browser, import_file):
    """It allows to upload, edit, list and delete files for import."""
    browser.login('mgr')
    browser.open(browser.MASTER_DATA_URL)
    # Overview is empty by default
    browser.getLink('Import data').click()
    assert browser.IMPORTER_OVERVIEW_URL == browser.url
    assert "No import files uploaded, yet" in browser.contents
    # Create a file
    browser.getLink('file').click()
    assert browser.IMPORTER_FILE_ADD_URL == browser.url
    browser.getControl('file').add_file(
        import_file('Import data file'), 'text/plain', 'file.txt')
    browser.getControl('Add').click()
    assert '"file.txt" added.' == browser.message
    # List the file
    assert browser.IMPORTER_OVERVIEW_URL == browser.url
    assert '>file.txt</a>' in browser.contents
    assert browser.IMPORTER_FILE_IMPORT_URL == browser.getLink('Import').url
    # Read the uploaded file
    browser.getLink('file.txt').click()
    assert browser.IMPORTER_FILE_EDIT_URL == browser.url
    assert browser.getControl('name').value == 'file.txt'
    assert 'text/plain' == browser.getControl('Mime Type').value
    browser.getLink('Download file').click()
    assert browser.IMPORTER_FILE_DOWNLOAD_URL == browser.url
    assert 'text/plain' == browser.headers['content-type']
    assert ('attachment; filename=file.txt' ==
            browser.headers['content-disposition'])
    assert 'Import data file' == browser.contents
    # It is possible to upload a new file instead of the previously uploaded
    # one:
    browser.open(browser.IMPORTER_FILE_EDIT_URL)
    browser.getControl('file', index=1).add_file(
        import_file('Import2 data2 file2'), 'text/csv', 'file2.csv')
    browser.getControl('Apply').click()
    assert 'Data successfully updated.' == browser.message
    assert browser.IMPORTER_OVERVIEW_URL == browser.url
    # Delete file
    browser.getLink('Delete').click()
    assert browser.IMPORTER_FILE_DELETE_URL == browser.url
    browser.getControl('Yes').click()
    assert '"file2.csv" deleted.' == browser.message
    assert browser.IMPORTER_OVERVIEW_URL == browser.url
    # Get rid of flash message containing `file2.csv`:
    browser.open(browser.IMPORTER_OVERVIEW_URL)
    assert 'file2.csv' not in browser.contents


def test_importer__Overview__1(address_book, browser, importer_link):
    """There is a link to it rendered in master data for admin."""
    browser.login('mgr')
    browser.open(browser.MASTER_DATA_URL)
    assert ([importer_link] in
            [browser.etree_to_list(x) for x in browser.etree.xpath('//li/a')])


@pytest.mark.parametrize('role', ['editor', 'visitor'])
def test_importer__Overview__2(address_book, browser, importer_link, role):
    """There is a no link to it rendered in master data for some roles."""
    browser.login(role)
    browser.open(browser.MASTER_DATA_URL)
    assert ([importer_link] not in
            [browser.etree_to_list(x) for x in browser.etree.xpath('//li/a')])


@pytest.mark.parametrize('role', ['editor', 'visitor'])
def test_importer__Overview__3(address_book, browser, role):
    """It is not allowed to be accessed by some user roles."""
    browser.login(role)
    with pytest.raises(HTTPError) as err:
        browser.open(browser.IMPORTER_OVERVIEW_URL)
    assert 'HTTP Error 403: Forbidden' == str(err.value)


@pytest.mark.parametrize('role', ['editor', 'visitor'])
def test_importer__Add__1(address_book, browser, role):
    """It is not allowed to be accessed by some user roles."""
    browser.login(role)
    with pytest.raises(HTTPError) as err:
        browser.open(browser.IMPORTER_FILE_ADD_URL)
    assert 'HTTP Error 403: Forbidden' == str(err.value)


def test_importer__Add__2(address_book, browser, import_file):
    """It sets the interface `IImportFile` on the created file."""
    browser.login('mgr')
    browser.open(browser.IMPORTER_FILE_ADD_URL)
    browser.getControl('file').add_file(
        import_file('Import data file'), 'text/plain', 'file.txt')
    browser.getControl('Add').click()
    assert '"file.txt" added.' == browser.message
    assert IImportFile.providedBy(address_book.importer['File'])


@pytest.mark.parametrize('role', ['editor', 'visitor'])
def test_importer__Edit__1(address_book, browser, role):
    """It is not allowed to be accessed by some user roles."""
    browser.login(role)
    with pytest.raises(HTTPError) as err:
        browser.open(browser.IMPORTER_FILE_EDIT_URL)
    assert 'HTTP Error 403: Forbidden' == str(err.value)


@pytest.mark.parametrize('role', ['editor', 'visitor'])
def test_importer__Delete__1(address_book, browser, role):
    """It is not allowed to be accessed by some user roles."""
    browser.login(role)
    with pytest.raises(HTTPError) as err:
        browser.open(browser.IMPORTER_FILE_DELETE_URL)
    assert 'HTTP Error 403: Forbidden' == str(err.value)
