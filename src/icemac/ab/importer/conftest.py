from icemac.ab.importer.browser.importer import provide_IImportFile
import icemac.ab.importer
import icemac.ab.importer.testing
import icemac.addressbook.testing
import pytest



pytest_plugins = 'icemac.addressbook.fixtures'

# Fixtures to set-up infrastructure which are usable in tests:


@pytest.yield_fixture(scope='function')
def address_book(addressBookConnectionF):
    """Get the address book with importer as site."""
    for address_book in icemac.addressbook.testing.site(
            addressBookConnectionF):
        yield address_book


@pytest.fixture(scope='function')
def browser(browserWsgiAppS):
    """Fixture for testing with zope.testbrowser."""
    assert icemac.addressbook.testing.CURRENT_CONNECTION is not None, \
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


# Fixtures to help asserting

@pytest.fixture(scope='function')
def sitemenu(browser):
    """Helper fixture to test the selections in the site menu."""
    return icemac.addressbook.testing.SiteMenu


@pytest.fixture(scope='function')
def assert_address_book(address_book):
    """Fixture returning an object providing a custom address book asserts."""
    return icemac.addressbook.testing.AddressBookAssertions(address_book)


# Infrastructure fixtures


@pytest.yield_fixture(scope='session')
def zcmlS():
    """Load importer ZCML on session scope."""
    layer = icemac.addressbook.testing.SecondaryZCMLLayer(
        'Importer', __name__, icemac.ab.importer)
    layer.setUp()
    yield layer
    layer.tearDown()


@pytest.yield_fixture(scope='session')
def zodbS(zcmlS):
    """Create an empty test ZODB."""
    for zodb in icemac.addressbook.testing.pyTestEmptyZodbFixture():
        yield zodb


@pytest.yield_fixture(scope='session')
def addressBookS(zcmlS, zodbS):
    """Create an address book for the session."""
    for zodb in icemac.addressbook.testing.pyTestAddressBookFixture(
            zodbS, 'ImporterS'):
        yield zodb


@pytest.yield_fixture(scope='function')
def addressBookConnectionF(addressBookS):
    """Get the connection to the right demo storage."""
    for connection in icemac.addressbook.testing.pyTestStackDemoStorage(
            addressBookS, 'ImporterF'):
        yield connection
