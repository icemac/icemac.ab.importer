# -*- coding: utf-8 -*-
# Copyright (c) 2009-2010 Michael Howitz
# See also LICENSE.txt

from icemac.addressbook.i18n import MessageFactory as _
import icemac.ab.importer.browser.wizard.base
import icemac.addressbook.browser.file.file
import icemac.addressbook.file.interfaces


class EditFile(icemac.ab.importer.browser.wizard.base.Step):

    interface = icemac.addressbook.file.interfaces.IFile
    label = _(u'Edit import file')

    @property
    def available(self):
        return icemac.ab.importer.browser.wizard.base.get_file_session(
            self.context, self.request).get('edit_file_available', False)

    def applyChanges(self, data):
        super(EditFile, self).applyChanges(data)
        icemac.addressbook.browser.file.file.update_blob(
            self.widgets['data'], self.context)
