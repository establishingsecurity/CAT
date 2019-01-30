import logging

from .utils.checkresult import CheckResult, Severity
from .oracle import Oracle

# use pathlib.Path in python2.7
try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

__version__ = "0.0.1"

logging.getLogger(__name__).addHandler(logging.NullHandler())
