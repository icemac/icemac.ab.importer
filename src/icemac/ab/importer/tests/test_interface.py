# -*- coding: utf-8 -*-
# Copyright (c) 2008-2010 Michael Howitz
# See also LICENSE.txt

import unittest
import zope.interface.verify
import icemac.ab.importer.interfaces
import icemac.ab.importer.importer


class TestInterfaces(unittest.TestCase):

    def test_importer(self):
        zope.interface.verify.verifyObject(
            icemac.ab.importer.interfaces.IImporter,
            icemac.ab.importer.importer.Importer())
