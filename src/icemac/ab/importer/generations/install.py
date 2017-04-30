import icemac.ab.importer.install
import icemac.addressbook.addressbook
import icemac.addressbook.generations.utils


@icemac.addressbook.generations.utils.evolve_addressbooks
def evolve(address_book):
    """Install the importer into each existing address book."""
    icemac.ab.importer.install.install_importer(
        icemac.addressbook.addressbook.AddressBookCreated(address_book))
