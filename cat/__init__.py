import sys
import logging

if sys.version_info.major >= 3:
    from pathlib import Path
else:
    from pathlib2 import Path


from .oracle import Oracle
from .utils.result import Result, Severity

__version__ = "0.0.1"

logging.getLogger(__name__).addHandler(logging.NullHandler())
