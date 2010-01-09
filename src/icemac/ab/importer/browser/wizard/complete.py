# -*- coding: utf-8 -*-
# Copyright (c) 2009-2010 Michael Howitz
# See also LICENSE.txt

from icemac.addressbook.i18n import MessageFactory as _
import zope.traversing.api
import zope.traversing.browser.absoluteurl
import z3c.wizard.step


class Complete(z3c.wizard.step.Step):

    label = _(u'Complete')

    def applyChanges(self, data):
        super(Complete, self).applyChanges(data)
        self.wizard.nextURL = zope.traversing.browser.absoluteurl.absoluteURL(
            zope.traversing.api.getParent(self.context), self.request)
