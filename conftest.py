import pytest

from cat.log import enable_logging


def pytest_addoption(parser):
    parser.addoption(
        "--enable-logs",
        "--enable-logging",
        action="store_true",
        default=False,
        help="enable logging output (use together with -s)",
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--enable-logs"):
        enable_logging()
