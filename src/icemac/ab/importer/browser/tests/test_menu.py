from __future__ import unicode_literals
import pytest


@pytest.fixture(scope='function')
def md_menu(address_book, browser, sitemenu):
    """Fixture to test the master data menu."""
    browser.login('mgr')
    return sitemenu(
        browser, 3, 'Master data', browser.IMPORTER_OVERVIEW_URL)


def test_menu__master_data_menu__1(md_menu):
    """The master data menu item is selected on the importer overview."""
    assert md_menu.item_selected(md_menu.menu_item_URL)


def test_menu__master_data_menu__2(md_menu, address_book, ImportFileFactory):
    """The master data menu item is selected on the import file."""
    ImportFileFactory(address_book, u'file.csv', ['file contents'])
    assert md_menu.item_selected(md_menu.browser.IMPORTER_FILE_EDIT_URL)
