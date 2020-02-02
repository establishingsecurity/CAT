import logging
from pathlib import Path

from .oracle import Oracle
from .utils.result import Result, Severity

__version__ = "0.0.1"

logging.getLogger(__name__).addHandler(logging.NullHandler())
