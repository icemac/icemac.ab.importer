===========
 Changelog
===========

2.11 (unreleased)
=================

- Adapt code to `icemac.addressbook >= 9.2`.


2.10 (2019-09-28)
=================

- Adapt to new feature in `icemac.addressbook 9.0`: customization of the labels
  of pre-defined fields:

    + use customized labels in import forms

    + do not use field label customizations which are set for file fields on
      fields of import files.

- Adapt tests to `icemac.addressbook >= 9.0`.

2.9 (2018-10-13)
================

- Improve naming of import fields and add descriptions to them.

- Fix wording mess of import file readers, they are now named as file formats.

- Update to changes in test infrastructure in `icemac.addressbook >= 8.0`.

- Change installation procedure from `bootstrap.py` to `virtualenv`,
  see `README.txt`.


Previous versions
=================

See ``OLD_CHANGES.rst`` inside the package.
