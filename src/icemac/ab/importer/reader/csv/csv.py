# -*- coding: utf-8 -*-
# Copyright (c) 2009-2010 Michael Howitz
# See also LICENSE.txt

from __future__ import absolute_import
from icemac.addressbook.i18n import MessageFactory as _
import csv
import datetime
import icemac.ab.importer.reader.base
import time


def as_unicode(method):
    def decorated(*args):
        result = method(*args)
        encoding = args[0].encoding
        for value in result:
            yield unicode(value, encoding)
    return decorated


def as_data(method):
    def decorated(*args):
        def convert(value):
            if value == '':
                return None
            try:
                time_tuple = time.strptime(value.strip(), date_format)
            except:
                # no date value, do normal convert
                return unicode(value, encoding)
            else:
                return datetime.date(*time_tuple[:3])

        result = method(*args)
        encoding = args[0].encoding
        date_format = args[0].date_format
        for value in result:
            yield [convert(x) for x in value]

    return decorated


class CSV(icemac.ab.importer.reader.base.BaseReader):
    "Read CSV import files."

    title = _(u'CSV file (comma separated fields, ISO-dates, UTF-8 encoded)')
    encoding = 'utf-8'
    date_format = '%Y-%m-%d'

    def _getReader(self):
        self.file.seek(0)
        return csv.reader(self.file)

    @as_unicode
    def getFieldNames(self):
        # get only first line, as it contains the field names
        return self._getReader().next()

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

    @as_data
    def __iter__(self):
        reader = self._getReader()
        # skip first line (field names)
        reader.next()
        for fields in reader:
            yield fields
