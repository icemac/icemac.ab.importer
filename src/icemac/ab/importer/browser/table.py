# -*- coding: utf-8 -*-
# Copyright (c) 2009-2010 Michael Howitz
# See also LICENSE.txt

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


