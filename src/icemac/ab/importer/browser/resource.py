# -*- coding: utf-8 -*-
# Copyright (c) 2010 Michael Howitz
# See also LICENSE.txt

import hurry.resource
import os.path

res = hurry.resource.Library('import', 'resources')
import_css = hurry.resource.ResourceInclusion(res, 'import.css')
