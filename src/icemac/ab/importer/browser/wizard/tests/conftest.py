from icemac.addressbook.interfaces import IPerson
from icemac.addressbook.interfaces import IPhoneNumber, IPostalAddress
import pytest


@pytest.fixture('function')
def some_user_defined_fields(address_book, FieldFactory):
    """Create some user defined fields."""
    FieldFactory(address_book, IPerson, u'Bool', u'photo permission?')
    FieldFactory(address_book, IPerson, u'Datetime', u'last seen')
    FieldFactory(address_book, IPostalAddress, u'Choice', u'state',
                 values=[u'Sachsen', u'Sachsen-Anhalt', u'Brandenburg'])
    FieldFactory(address_book, IPostalAddress, u'Int', u'number of letters')
    FieldFactory(address_book, IPhoneNumber, u'Decimal', u'cost per minute')
    FieldFactory(address_book, IPhoneNumber, u'Text', u'mail box text')
