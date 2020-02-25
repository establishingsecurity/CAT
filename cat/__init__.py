import logging

from .utils.result import Result, Severity
from .oracle import Oracle

# use pathlib.Path in python2.7
try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

__version__ = "0.2.0"

logging.getLogger(__name__).addHandler(logging.NullHandler())
