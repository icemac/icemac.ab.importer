from icemac.addressbook.addressbook import AddressBookCreated
from icemac.ab.importer.install import install_importer
from icemac.ab.importer.interfaces import IImporter


def test_install__install_importer__1(assert_address_book):
    """It creates an importer attribute."""
    install_importer(AddressBookCreated(assert_address_book.address_book))
    assert_address_book.has_attribute('importer', IImporter)


def test_install__install_importer__2(assert_address_book):
    """It does not break if it gets called twice."""
    event = AddressBookCreated(assert_address_book.address_book)
    install_importer(event)
    install_importer(event)
    assert_address_book.has_attribute('importer', IImporter)
