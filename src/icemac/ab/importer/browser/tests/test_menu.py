from __future__ import unicode_literals
import icemac.addressbook.browser.testing
import icemac.ab.importer.testing


class MasterDataSelectedCheckerTests(
        icemac.addressbook.browser.testing.SiteMenuTestMixIn,
        icemac.addressbook.testing.BrowserTestCase):
    """Testing ..menu.importer_views"""

    layer = icemac.ab.importer.testing.TEST_BROWSER_LAYER

    menu_item_index = 3
    menu_item_title = 'Master data'
    menu_item_URL = 'http://localhost/ab/++attribute++importer'
    login_as = 'mgr'

    def test_master_data_tab_is_selected_on_importer_master_data_overview(
            self):
        self.browser.open(self.menu_item_URL)
        self.assertIsSelected()

    def test_master_data_tab_is_selected_on_import_file(self):
        from zope.publisher.browser import TestRequest
        from zope.interface import alsoProvides
        from z3c.form.interfaces import IFormLayer
        request = TestRequest()
        alsoProvides(request, IFormLayer)
        view = icemac.addressbook.browser.file.file.Add(
            self.layer['addressbook'].importer, request)
        view.update()
        view.createAndAdd({})
        self.browser.open(
            'http://localhost/ab/++attribute++importer/File')
        self.assertIsSelected()
