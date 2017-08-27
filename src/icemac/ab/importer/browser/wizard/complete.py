# -*- coding: utf-8 -*-
from icemac.addressbook.i18n import _
import icemac.addressbook.browser.wizard
import zope.traversing.api
import zope.traversing.browser.absoluteurl


class Complete(icemac.addressbook.browser.wizard.Step):
    """Step displaying that the import was completed."""

    title = label = _(u'Complete')
    fields = {}

    def applyChanges(self, data):
        super(Complete, self).applyChanges(data)
        self.wizard.nextURL = zope.traversing.browser.absoluteurl.absoluteURL(
            zope.traversing.api.getParent(self.context), self.request)
