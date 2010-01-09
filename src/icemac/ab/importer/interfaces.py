# -*- coding: utf-8 -*-
# Copyright (c) 2009-2010 Michael Howitz
# See also LICENSE.txt

import zope.interface
import zope.schema


class IImporter(zope.interface.Interface):
    """Importer and storage for import files."""

    file_marker_interface = zope.interface.Attribute(
        u"""Interface to be used as marker interface for contained files.""")


class IImportFileContainer(zope.interface.Interface):
    "Marker interface for container which can contain files."


class IImportFile(zope.interface.Interface):
    """Marker interface for import files."""


class IImportFileReader(zope.interface.Interface):
    """Reader for an import file."""

    title = zope.schema.TextLine(
        title=u"User understandable name of the reader.", readonly=True)

    def canRead(file_handle):
        """Tell whether this reader is able to read the given file.

        A reader is able to read a file when:

          - it can open it successfully and

          - `getFieldNames` returns at least one field.

        When an exception occorures, the reader is not able to read the file,
        too.

        This method is a class method!

        """

    def open(file_handle):
        """Create a new file reader and use `file_handle` to read from.

        This method is a class method!

        """

    def getFieldNames():
        """Get an iterable of the names of the fields in the file.

        The names are unicode strings.

        """

    def getFieldSamples(field_name):
        """Get an iterable of up to three sample values for a field.

        The values are unicode strings.
        Date values are represented as ISO-date resp. empty string.

        """

    def __iter__():
        """Iterate over the file.

        Yields a list for each data row in the file. The values are unicode
        strings or `None`.  Date values are `datetime.date` objects or
        `None`.

        The indexes are the indexes of the corresponding field names in
        `getFieldNames`.

        """
