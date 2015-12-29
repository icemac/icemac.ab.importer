from icemac.ab.importer.browser.importer import provide_IImportFile
import icemac.ab.importer
import icemac.ab.importer.testing
import icemac.addressbook.testing
import pytest


pytest_plugins = 'icemac.addressbook.conftest'


# Fixtures to set-up infrastructure which are usable in tests:


@pytest.yield_fixture(scope='function')
def address_book(addressBookConnectionF):
    """Get the address book with importer as site."""
    for address_book in icemac.addressbook.conftest.site(
            addressBookConnectionF):
        yield address_book


@pytest.fixture(scope='function')
def browser(browserWsgiAppS):
    """Fixture for testing with zope.testbrowser."""
    assert icemac.addressbook.conftest.CURRENT_CONNECTION is not None, \
        "The `browser` fixture needs a database fixture like `address_book`."
    return icemac.ab.importer.testing.Browser(wsgi_app=browserWsgiAppS)


@pytest.fixture(scope='session')
def ImportFileFactory(FileFactory):
    """Create an import file in the importer.

    data ... list of the lines in the import file.
    """
    def create_file(address_book, filename, data, **kw):
        file = FileFactory(
            address_book.importer, filename, data='\n'.join(data), **kw)
        provide_IImportFile(file)
        return file
    return create_file


# Infrastructure fixtures


@pytest.yield_fixture(scope='session')
def zcmlS(zcmlS):
    """Load importer ZCML on session scope."""
    layer = icemac.addressbook.testing.SecondaryZCMLLayer(
        'Importer', __name__, icemac.ab.importer, [zcmlS])
    layer.setUp()
    yield layer
    layer.tearDown()


@pytest.yield_fixture(scope='session')
def addressBookS(zcmlS, zodbS):
    """Create an address book for the session."""
    for zodb in icemac.addressbook.conftest.pyTestAddressBookFixture(
            zodbS, 'ImporterS'):
        yield zodb


@pytest.yield_fixture(scope='function')
def addressBookConnectionF(addressBookS):
    """Get the connection to the right demo storage."""
    for connection in icemac.addressbook.conftest.pyTestStackDemoStorage(
            addressBookS, 'ImporterF'):
        yield connection
