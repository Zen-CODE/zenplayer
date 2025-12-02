"""A module designed to insert Mock classes to remove dependencies for Android."""

from unittest.mock import MagicMock
import sys
from types import ModuleType


def mock_package(package_name: str) -> ModuleType:
    mock_package = ModuleType(package_name)
    mock_package.__path__ = [package_name]
    sys.modules[package_name] = mock_package
    return mock_package


def mock_submodule(sub_module_name: str) -> MagicMock:
    mock_sm = MagicMock(name=sub_module_name)
    sys.modules[sub_module_name] = mock_sm
    return mock_sm


mock_package("pynput")
mock_submodule("pynput.keyboard")
mock_submodule("components.keyboard_handler")

mock_package("vlc")
mock_submodule("vlc.EventType")
mock_submodule("vlc.Instance")
