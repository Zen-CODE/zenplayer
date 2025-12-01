"""A module designed to insert Mock classes to remove dependencies for Android."""

from unittest.mock import MagicMock
import sys
from types import ModuleType

PACKAGE_NAME = "pynput"
mock_package = ModuleType(PACKAGE_NAME)
mock_package.__path__ = [PACKAGE_NAME]
sys.modules[PACKAGE_NAME] = mock_package

zen_mock = MagicMock(name="ZenMock")

# 6. Create the full name for the submodule
SUBMODULE_NAME = f"{PACKAGE_NAME}.keyboard"

# 7. Insert the submodule content into sys.modules
sys.modules[SUBMODULE_NAME] = zen_mock
print(f"Successfully inserted submodule '{SUBMODULE_NAME}'.")
