import pytest


@pytest.mark.parametrize('role', ['editor', 'visitor'])
def test_base__ImportWizard__1(address_book, browser, role):
    """It is not allowed to be accessed by some user roles."""
    browser.login(role)
    browser.assert_forbidden(browser.IMPORTER_FILE_IMPORT_URL)
