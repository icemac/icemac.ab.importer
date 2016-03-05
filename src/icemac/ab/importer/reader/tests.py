# -*- coding: utf-8 -*-
from icemac.ab.importer.reader.base import BaseReader
from mock import patch
import icemac.ab.importer.interfaces
import pytest
import zope.interface.verify


def test_base__BaseReader__1():
    """It fulfills the `IImportFileReader` interface."""
    assert zope.interface.verify.verifyObject(
        icemac.ab.importer.interfaces.IImportFileReader, BaseReader())


def test_base__BaseReader__canRead__1():
    """It returns `False` on an exception during calling `open()`."""
    with patch.object(BaseReader, 'open', side_effect=Exception):
        assert False is BaseReader.canRead(None)


def test_base__BaseReader__canRead__2():
    """It returns `False` on an exception during calling `getFieldNames()`."""
    with patch.object(BaseReader, 'getFieldNames', side_effect=Exception):
        assert False is BaseReader.canRead(None)


def test_base__BaseReader__canRead__3():
    """It returns `False` if `getFieldNames()` returns an empty list."""
    with patch.object(BaseReader, 'getFieldNames', return_value=[]):
        assert False is BaseReader.canRead(None)


def test_base__BaseReader__canRead__4():
    """It returns `True` if `getFieldNames()` returns an non-empty list."""
    with patch.object(BaseReader, 'getFieldNames', return_value=['sdfg']):
        assert True is BaseReader.canRead(None)


def test_base__BaseReader__getFieldNames__1():
    """It is not implemented."""
    with pytest.raises(NotImplementedError):
        BaseReader().getFieldNames()


def test_base__BaseReader__getFieldSamples__1():
    """It is not implemented."""
    with pytest.raises(NotImplementedError):
        BaseReader().getFieldSamples(None)


def test_base__BaseReader____iter____1():
    """It is not implemented."""
    with pytest.raises(NotImplementedError):
        BaseReader().__iter__()
