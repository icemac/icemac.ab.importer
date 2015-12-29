import icemac.addressbook.testing


class Browser(icemac.addressbook.testing.Browser):
    """Browser adapted for importer."""

    IMPORTER_OVERVIEW_URL = 'http://localhost/ab/++attribute++importer'

    IMPORTER_FILE_ADD_URL = (
        'http://localhost/ab/++attribute++importer/@@addFile.html')
    IMPORTER_FILE_IMPORT_URL = (
        'http://localhost/ab/++attribute++importer/File/@@import')
    IMPORTER_IMPORT_EDIT_URL = (
        'http://localhost/ab/++attribute++importer/File/import/editFile')
    IMPORTER_IMPORT_READER_URL = (
        'http://localhost/ab/++attribute++importer/File/import/reader')
    IMPORTER_IMPORT_MAP_URL = (
        'http://localhost/ab/++attribute++importer/File/import/map')
    IMPORTER_IMPORT_REVIEW_URL = (
        'http://localhost/ab/++attribute++importer/File/import/review')
    IMPORTER_IMPORT_COMPLETE_URL = (
        'http://localhost/ab/++attribute++importer/File/import/complete')
    IMPORTER_FILE_EDIT_URL = 'http://localhost/ab/++attribute++importer/File'
    IMPORTER_FILE_DOWNLOAD_URL = (
        'http://localhost/ab/++attribute++importer/File/download.html')
    IMPORTER_FILE_DELETE_URL = (
        'http://localhost/ab/++attribute++importer/File/@@delete.html')

    IMPORTER_READERS_LIST_URL = (
        'http://localhost/ab/++attribute++importer/@@readers.html')
