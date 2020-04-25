from __future__ import absolute_import
from icemac.addressbook.i18n import _
import csv
import datetime
import functools
import icemac.ab.importer.reader.base
import time
import six


def as_unicode(method):  # drop together with PY2
    def decorated(*args):
        result = method(*args)
        if six.PY2:  # pragma: no cover
            encoding = args[0].encoding
            for value in result:
                yield six.text_type(value, encoding)
        else:  # pragma: no cover
            for value in result:
                yield value
    return decorated


def as_data(method):
    @functools.wraps(method)
    def decorated(*args):
        def convert(value):
            if value == '':
                return None
            try:
                time_tuple = time.strptime(value.strip(), date_format)
            except Exception:
                if six.PY2:  # pragma: no cover
                    value = six.text_type(value, encoding)
                return value
            else:
                return datetime.date(*time_tuple[:3])

        result = method(*args)
        encoding = args[0].encoding
        date_format = args[0].date_format
        for value in result:
            yield [convert(x) for x in value]

    return decorated


class BytesToTextStream(object):
    """Convert a bytes stream into a text stream."""

    def __init__(self, bytes_stream, encoding):
        self.bytes_stream = bytes_stream
        self.encoding = encoding

    def __iter__(self):
        return self

    def __next__(self):
        chunk = next(self.bytes_stream)
        if six.PY3:  # pragma: no cover
            chunk = chunk.decode(self.encoding)
        return chunk

    if six.PY2:  # pragma: no cover
        next = __next__


class CSV(icemac.ab.importer.reader.base.BaseReader):
    """Read CSV import files."""

    title = _(u'CSV file (comma separated fields, ISO-dates, UTF-8 encoded)')
    encoding = 'utf-8'
    date_format = '%Y-%m-%d'

    def _getReader(self):
        self.file.seek(0)
        return csv.reader(BytesToTextStream(self.file, self.encoding))

    @as_unicode
    def getFieldNames(self):
        # get only first line, as it contains the field names
        return next(self._getReader())

    @as_unicode
    def getFieldSamples(self, field_name):
        index = list(self.getFieldNames()).index(field_name)
        reader = self._getReader()
        # skip first line (field names)
        next(reader)
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
        next(reader)
        for fields in reader:
            yield fields
