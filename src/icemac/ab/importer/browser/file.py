from icemac.addressbook.i18n import _
import icemac.addressbook.browser.base
import icemac.addressbook.browser.file.file
import icemac.addressbook.file.interfaces


class Edit(icemac.addressbook.browser.base.BaseEditForm):
    """Edit an import file."""

    interface = icemac.addressbook.file.interfaces.IFile
    next_url = 'parent'
    label = _('Edit file')

    def applyChanges(self, data):
        changes = super(Edit, self).applyChanges(data)
        icemac.addressbook.browser.file.file.update_blob(
            self.widgets['data'], self.context)
        return changes
