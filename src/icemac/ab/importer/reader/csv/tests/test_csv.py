# -*- coding: utf-8 -*-
# Copyright (c) 2009-2010 Michael Howitz
# See also LICENSE.txt

import icemac.ab.importer.reader.testing
import icemac.ab.importer.reader.csv.csv


class CSVTest(icemac.ab.importer.reader.testing.ReaderTest):

    reader_class = icemac.ab.importer.reader.csv.csv.CSV
    import_file = 'long.csv'
    import_file_short = 'short.csv'
