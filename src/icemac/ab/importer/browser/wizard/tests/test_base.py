from mechanize import HTTPError
import pytest


@pytest.mark.parametrize('role', ['editor', 'visitor'])
def test_base__ImportWizard__1(address_book, browser, role):
    """It is not allowed to be accessed by some user roles."""
    browser.login(role)
    with pytest.raises(HTTPError) as err:
        browser.open(browser.IMPORTER_FILE_IMPORT_URL)
    assert 'HTTP Error 403: Forbidden' == str(err.value)
