===========
Old changes
===========

Changelog of releases more than 2 major versions behind current version.

2.1.0 (2014-07-01)
==================

- The master data tab in the main menu is now highlighted when the importer
  is displayed.

- Update code and tests to changes in `icemac.addressbook 2.5`.

- Add `py.test` to run the tests.


2.0.0 (2013-11-03)
==================

- Updated supported Python version to 2.7.x.

- Adapted test setup and tests to `icemac.addressbook` version 2.0.


1.10.0 (2013-06-13)
===================

- Adapted configuration, tests and test set up to run with
  `icemac.addressbook` version 1.10.

- Moved repository to https://bitbucket.org/icemac/icemac.ab.importer

1.9.0 (2012-12-29)
==================

- Adapted tests to run with `icemac.addressbook` version 1.9.


1.8.1 (2012-04-20)
==================

- Adapted test set up to run with `icemac.addressbook` version 1.8.1.


1.8.0 (2011-12-14)
==================

- Adapted tests and test set up to run with `icemac.addressbook` version 1.8.


1.7.2 (2011-11-22)
==================

- Fixed a missing import which was masked by the Python import bug.

1.7.1 (2011-11-03)
==================

- Fixing brown bag release: only namespace packages were installed.


1.7.0 (2011-11-03)
==================

- Using stacked test layers for faster tests.

- Extracted reuseable parts of import wizard to `icemac.addressbook`.

- Adapted code, test set up and tests to run with `icemac.addressbook` version
  1.7.

1.6.0 (2011-02-03)
==================

- Adapted code and tests to run with `icemac.addressbook` version 1.6.


1.5.0 (2010-11-23)
==================

- Adapted tests and code to run with `icemac.addressbook` version 1.5.

- Dropped `zope.app.testing` test dependency.

- Moved CSS statements to separate file.


1.4.0 (2010-08-19)
==================

- Adapted code and tests to run with `icemac.addressbook` version 1.4.


1.3.0 (2010-03-20)
==================

- Adapted code and tests to run with `icemac.addressbook` newer than
  version 1.2.0.


1.2.0 (2010-02-06)
==================

- Fixed tests to run together with `icemac.addressbook` version 1.1
  and above.


1.1.0 (2009-12-29)
==================

- Prepared texts for translation.


1.0.1 (2009-12-20)
==================

- Importing persons, deleting them and importing them again, led to an
  exception.


1.0 (2009-11-21)
================

- Supporting the user defined fields feature of address book.

- Added migration code to add importer to exising address books.

0.9.1 (2009-09-28)
==================

- Fixing brown bag release: only namespace packages were installed.


0.9 (2009-09-28)
================

- Extracted importer from icemac.addressbook, to make it optional and
  easily extendable.
