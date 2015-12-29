from StringIO import StringIO
import pytest


@pytest.fixture('session')
def import_file():
    """Get a function to create a file like object for import."""
    def create_file(data):
        file = StringIO()
        file.write(data)
        file.seek(0)
        return file
    return create_file
