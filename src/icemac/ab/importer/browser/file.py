from icemac.addressbook.i18n import _
import icemac.ab.importer.interfaces
import icemac.addressbook.browser.base
import icemac.addressbook.browser.file.file


class Edit(icemac.addressbook.browser.base.BaseEditForm):
    """Edit an import file."""

    interface = icemac.ab.importer.interfaces.IImportFile
    title = _('Edit file')
    next_url = 'parent'

    def applyChanges(self, data):
        changes = super(Edit, self).applyChanges(data)
        icemac.addressbook.browser.file.file.update_blob(
            self.widgets['data'], self.context)
        return changes
