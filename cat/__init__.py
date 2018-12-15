import logging

from .utils.checkresult import CheckResult, Severity
from .oracle import Oracle

__version__ = "0.0.1"

logging.getLogger(__name__).addHandler(logging.NullHandler())
