import logging
import sys

from .utils.result import Result, Severity

# mypy: ignore-errors
if sys.version_info.major >= 3:
    from pathlib import Path
else:
    from pathlib2 import Path

__version__ = "0.2.0"

logging.getLogger(__name__).addHandler(logging.NullHandler())
