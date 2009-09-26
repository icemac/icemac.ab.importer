# -*- coding: utf-8 -*-
# Copyright (c) 2009 Michael Howitz
# See also LICENSE.txt

import icemac.addressbook.interfaces
import pytz
import z3c.table.column


class ModifiedColumnLocalTime(z3c.table.column.ModifiedColumn):
    """Modification date in local time of the browser."""

    def getValue(self, item):
        value = super(ModifiedColumnLocalTime, self).getValue(item)
        if value:
            timezones = self.request.locale.dates.timezones
            timezone = None
            for tz in timezones.values():
                if tz.type:
                    timezone = tz.type
            if timezone:
                timezone = pytz.timezone(timezone)
                value = value.astimezone(timezone)
        return value


class GetAttrColumn(z3c.table.column.GetAttrColumn):
    "GetAttrColumn which does not display `None` but empty string instead."

    def getValue(self, obj):
        value = super(GetAttrColumn, self).getValue(obj)
        if value is None:
            value = u''
        return value


class AttrGetAttrColumn(GetAttrColumn):
    """Fetch the object on the attribute named `masterAttrName` and select the
    attribute `attrName` on it."""

    masterAttrName = None

    def getValue(self, obj):
        master_obj = getattr(obj, self.masterAttrName, None)
        return super(AttrGetAttrColumn, self).getValue(master_obj)


class CountryAttrGetAttrColumn(AttrGetAttrColumn):
    """AttrGetAttrColumn for gocept.country objects."""

    def getValue(self, obj):
        country = super(CountryAttrGetAttrColumn, self).getValue(obj)
        if country != u'':
            # country set
            country = country.token
        return country


class KeywordsGetAttrColumn(z3c.table.column.GetAttrColumn):
    """GetAttrColumn where attr is an iterable of keywords."""

    def getValue(self, obj):
        values = super(KeywordsGetAttrColumn, self).getValue(obj)
        return u', '.join(
            icemac.addressbook.interfaces.ITitle(x) for x in values)
