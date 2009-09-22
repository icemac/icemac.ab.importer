This package provides import infrastructure for `icemac.addressbook`_.

.. _`icemac.addressbook` : http://pypi.python.org/pypi/icemac.addressbook

.. contents::

=========
 Concept
=========

Importing data follows these steps:

- An administrative user uploads an import file to the address
  book. It gets stored there inside the importer.

- When the user decides to import the data inside this uploaded file,
  he is presented with a list of import file readers which claim to be
  able to read the import file.

- After choosing the import file reader the user has to map which
  field data in the import file should be stored in which field in the
  address book.

- The imported data gets shown and the user can decide to keep or to
  discard the imported data.

===================================
 Write your own import file reader
===================================

The key to extend the import mechanism is to provide a reader for the
needed import file type.

This package already provides an import file reader for CSV files.

`icemac.ab.importxls` provides a reader for XLS files, so it could be
a starting point, too.

Write a reader class
====================

The reader class must implement the interface
``icemac.ab.importer.interfaces.IImportFileReader``. There is a base
implementation in ``icemac.ab.importer.reader.base.BaseReader`` which
the new reader class can extend, so there are only four things left to
implement (see the interface for a more specific description):

- ``title`` attribute -- shown to the user in the choose reader dialog

- ``getFieldNames`` method -- lists the names of the fields in the
  import file

- ``getFieldSamples`` method -- gets samples of a specific field to
  ease the mapping task for the user

- ``__iter__`` method -- iterates the import file to get the data for
  the import.

The file for reading gets stored on the ``file`` attribute.


Test reader class
=================

``icemac.ab.importer.reader.testing.ReaderTest`` provides a (base)
test class which checks whether the reader behaves as expected. It
requires some example files for the reader. The derived reader tests
must fulfill the following conventions:

- The directory structure must look like this::

  |-reader.py
  |-tests
    |-__init__.py
    |-test_reader.py
    |-data
     |-short.file
     |-long.file

- The `__init__.py` file can be empty.

- The `test_reader.py` file contains the test class which extends
  ``icemac.ab.importer.reader.testing.BaseReaderTest``. Three
  attributes have to be set on this class:

  - ``reader_class`` - must point to the reader's class object

  - ``import_file`` - name of the longer import file (see below),
    without path

  - ``import_file_short`` name of the shorter import file (see below),
    without path

- There must be three files in the `data` dictionary:

  - a file for the ``import_file_short`` attribute on the test class,
    containing the following data:

    =========  ==========  =========
    firstname  birth_date  last name
               1976-01-24    Koch
    =========  ==========  =========

  - a file for the ``import_file`` attribute on the test class, containing the
    following data:

    =========  ==========  =========
    firstname  birth_date  last name
    Andreas    1976-01-24  Koch
    Hanna      2000-01-01  Hula
    Jens                   Jänsen
               2001-12-31  Fruma
    =========  ==========  =========


Register reader class
=====================

To register the reader class with `icemac.addressbook` write a `configure.zcml` file in the reader package::

  <configure xmlns="http://namespaces.zope.org/zope">
    <adapter
       name="<name>"
       factory="<path>" />
  </configure>

The ``name`` attribute contains a unique name to identify the importer
internally. The ``factory`` attribute contains the python path to the reader
class.

Integrate the reader in icemac.addressbook
==========================================

During installing `icemac.addressbook`, it is possible to enter the name of external dependencies. This is the place to integrate your reader into `icemac.addressbook`.

