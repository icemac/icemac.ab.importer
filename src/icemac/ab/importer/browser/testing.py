# -*- coding: latin-1 -*-
# Copyright (c) 2008-2009 Michael Howitz
# See also LICENSE.txt
# $Id$

import os.path
import zope.app.testing.functional


zope.app.testing.functional.defineLayer(
    'ImporterLayer', 'ftesting.zcml', allow_teardown=True)
