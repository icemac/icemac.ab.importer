# -*- coding: utf-8 -*-
from icemac.addressbook.i18n import _
import zope.traversing.api
import zope.traversing.browser.absoluteurl
import z3c.wizard.step


class Complete(z3c.wizard.step.Step):
    """Step displaying that the import was completed."""

    label = _(u'Complete')

    def applyChanges(self, data):
        super(Complete, self).applyChanges(data)
        self.wizard.nextURL = zope.traversing.browser.absoluteurl.absoluteURL(
            zope.traversing.api.getParent(self.context), self.request)
