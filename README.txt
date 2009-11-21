This package provides import infrastructure for `icemac.addressbook`_.

.. _`icemac.addressbook` : http://pypi.python.org/pypi/icemac.addressbook

.. contents::

=========
 Concept
=========

Importing data requires the following steps:

- A user having the `Administrator` role uploads an import file to the address
  book. It gets stored there inside the importer.

- When the user decides to import the the uploaded file,
  he is presented with a list of readers which claim to be
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

`icemac.ab.importxls`_ provides a reader for XLS files, so it could be
a starting point, too.

.. _icemac.ab.importxls: http://pypi.python.org/pypi/icemac.ab.importxls

1. Write a reader class
=======================

The reader class must implement the interface
``icemac.ab.importer.interfaces.IImportFileReader``. There is a base
implementation in ``icemac.ab.importer.reader.base.BaseReader`` which
the new reader class can extend, so there are only four things left to
implement (see the interface for a more specific description):

- ``title`` attribute -- shown to the user in the dialog when choosing
  the reader

- ``getFieldNames`` method -- lists the names of the fields in the
  import file

- ``getFieldSamples`` method -- returns samples of a specific field to
  ease the mapping task for the user

- ``__iter__`` method -- iterates the import file to get the data for
  the import.

The base class file stores the file for reading on the ``file`` attribute.


2. Test reader class
====================

``icemac.ab.importer.reader.testing.ReaderTest`` provides a (base)
test class which checks whether the reader behaves as expected. It
requires some example files for the reader. The derived reader tests
must fulfill the following conventions:

1. The directory structure must look like this: (directories in *italic*)

   - reader.py
   - *tests*

     - __init__.py
     - test_reader.py
     - *data*

       - short.file
       - long.file

2. The `__init__.py` file can be empty.

3. The `test_reader.py` file contains the test class which extends
   ``icemac.ab.importer.reader.testing.BaseReaderTest``. Three
   attributes have to be set on this class:

   - ``reader_class`` - must point to the reader's class object

   - ``import_file`` - name of the longer import file (see below),
     without path

   - ``import_file_short`` name of the shorter import file (see below),
     without path

4. There must be two files in the `data` directory:

   - a file for the ``import_file_short`` attribute on the test class,
     containing the following data:

     =============  =============  ==============
     **last name**  **firstname**  **birth_date**
     Koch                          1976-01-24
     =============  =============  ==============

   - a file for the ``import_file`` attribute on the test class, containing the
     following data:

     =============  =============  ==============
     **last name**  **firstname**  **birth_date**
     Koch           Andreas        1976-01-24
     Hula           Hanna          2000-01-01
     J |ae| nsen      Jens
     Fruma                         2001-12-31
     =============  =============  ==============

.. |ae| unicode:: U+000e4
   :trim:

3. Register the reader class
============================

To register the reader class with `icemac.addressbook` write a `configure.zcml` file in the reader package::

  <configure xmlns="http://namespaces.zope.org/zope">
    <include package="icemac.ab.importer" />
    <adapter
       name="<name>"
       factory="<path>" />
  </configure>

The ``icemac.ab.importer`` package is necessary to integrate the
importer UI into the address book.  The ``name`` attribute contains a
unique name to identify the importer internally. The ``factory``
attribute contains the python path to the reader class.

4. Create a python package
==========================

The reader class must be inside a python package. The package must
depend on ``icemac.ab.importer`` (``install_requires`` parameter in
`setup.py`).


5. Integrate the reader in icemac.addressbook
=============================================

During installing `icemac.addressbook`, it is possible to enter the
name of external dependencies. This is the place to integrate your
reader into `icemac.addressbook`.

