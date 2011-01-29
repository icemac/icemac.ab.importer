# -*- coding: utf-8 -*-
# Copyright (c) 2010-2011 Michael Howitz
# See also LICENSE.txt

import hurry.resource

res = hurry.resource.Library('import', 'resources')
import_css = hurry.resource.ResourceInclusion(res, 'import.css')
