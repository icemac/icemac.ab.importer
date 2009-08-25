# -*- coding: utf-8 -*-
# Copyright (c) 2009 Michael Howitz
# See also LICENSE.txt

from __future__ import absolute_import
from icemac.addressbook.i18n import MessageFactory as _
import csv
import icemac.ab.importer.reader.base


def as_unicode(method):
    def decorated(*args):
        result = method(*args)
        encoding = args[0].encoding
        for value in result:
            if isinstance(value, str):
                yield unicode(value, encoding)
            else:
                yield [unicode(x, encoding) for x in value]
    return decorated


class CSV(icemac.ab.importer.reader.base.BaseReader):
    "Read CSV import files."

    title = _(u'CSV file (UTF-8 encoded), comma separted fields')
    encoding = 'utf-8'

    def _getReader(self):
        self.file.seek(0)
        return csv.reader(self.file)

    @as_unicode
    def getFieldNames(self):
        return self._getReader().next() # first line

    @as_unicode
    def getFieldSamples(self, field_name):
        index = list(self.getFieldNames()).index(field_name)
        reader = self._getReader()
        # skip first line (field names)
        reader.next()
        num = 1
        for fields in reader:
            yield fields[index]
            if num >= 3:
                return
            num += 1

    @as_unicode
    def __iter__(self):
        reader = self._getReader()
        # skip first line (field names)
        reader.next()
        for fields in reader:
            yield fields
